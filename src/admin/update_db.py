from src.admin.parsers import BaseParser, ExcelParser
from src.config import settings
from src.core.cashe import Cache
from src.database import async_session_maker
from src.dishes.repositories import DishRepository
from src.dishes.schemas import CreateDish
from src.dishes.services import DishService
from src.menus.repositories import MenuRepository
from src.menus.schemas import MenuCreateInput
from src.menus.services import MenuService
from src.redis_conf import get_redis_connection
from src.submenus.repositories import SubMenuRepository
from src.submenus.schemas import SubMenuCreationInput
from src.submenus.services import SubMenuService


class UpdaterDB:
    def __init__(
            self,
            menu_service: MenuService,
            submenu_service: SubMenuService,
            dish_service: DishService,
            admin_parser: BaseParser,
    ):
        self.menu_service = menu_service
        self.submenu_service = submenu_service
        self.dish_service = dish_service
        self.admin_parser = admin_parser

    async def update_db_from_admin_data(self):
        """Update db from admin data."""
        db_data = await self._parse_db(await self.menu_service.get_with_relations())
        admin_data = await self.admin_parser.parse()
        db_data = await self._compare_and_update_menus(admin_data, db_data)
        db_data = await self._compare_and_update_submenus(admin_data, db_data)
        await self._compare_and_update_dishes(admin_data, db_data)
        await self._execute_background_tasks()

    async def _execute_background_tasks(self):
        """Execute background tasks of services."""
        await self.menu_service.background_tasks()
        await self.submenu_service.background_tasks()
        await self.dish_service.background_tasks()

    async def _compare_and_update_menus(self, admin_data: dict, db_data: dict) -> dict:
        """Update db menus from admin data."""
        for_create, for_update, for_delete = await self._find_difference(admin_data['menus'], db_data['menus'])
        await self._delete_objects(service=self.menu_service, objects=for_delete)
        await self._create_menus(menus=for_create)
        await self._update_menus(menus=for_update)
        return await self._remove_menu_childes(db_data, for_delete)

    async def _compare_and_update_submenus(self, admin_data: dict, db_data: dict) -> dict:
        """Update db submenus from admin data."""
        for_create, for_update, for_delete = await self._find_difference(admin_data['submenus'], db_data['submenus'])
        await self._delete_objects(service=self.submenu_service, objects=for_delete)
        await self._create_submenus(submenus=for_create)
        return await self._remove_submenu_childes(db_data, for_delete)

    async def _compare_and_update_dishes(self, admin_data: dict, db_data: dict) -> None:
        """Update db dishes from admin data."""
        for_create, for_update, for_delete = await self._find_difference(admin_data['dishes'], db_data['dishes'])
        await self._delete_objects(service=self.dish_service, objects=for_delete)
        await self._create_dishes(dishes=for_create)
        await self._update_dishes(dishes=for_update)

    async def _create_menus(self, menus: list):
        """Bulk create menus."""
        for menu in menus:
            uid = menu.pop('id')
            await self.menu_service.create(data=MenuCreateInput(**menu), id=uid)

    async def _create_submenus(self, submenus: list):
        """Bulk create submenus."""
        for submenu in submenus:
            uid = submenu.pop('id')
            menu_id = submenu.pop('menu_id')
            await self.submenu_service.create(data=SubMenuCreationInput(**submenu), menu_id=menu_id, id=uid)

    async def _create_dishes(self, dishes: list):
        """Bulk create dishes."""
        for dish in dishes:
            uid = dish.pop('id')
            menu_id = dish.pop('menu_id')
            submenu_id = dish.pop('submenu_id')
            await self.dish_service.create(data=CreateDish(**dish), id=uid, menu_id=menu_id, submenu_id=submenu_id)

    async def _update_menus(self, menus: list):
        """Bulk update menus."""
        for menu in menus:
            menu_id = menu.pop('id')
            await self.menu_service.update(data=MenuCreateInput(**menu), menu_id=menu_id)

    async def _update_submenus(self, submenus: list):
        """Bulk update submenus."""
        for submenu in submenus:
            submenu_id = submenu.pop('id')
            submenu.pop('menu_id')
            await self.submenu_service.update(data=SubMenuCreationInput(**submenu), submenu_id=submenu_id)

    async def _update_dishes(self, dishes: list):
        """Bulk update dishes."""
        for dish in dishes:
            dish_id = dish.pop('id')
            menu_id = dish.pop('menu_id')
            submenu_id = dish.pop('submenu_id')
            await self.dish_service.update(
                data=CreateDish(**dish), menu_id=menu_id, dish_id=dish_id, submenu_id=submenu_id,
            )

    @staticmethod
    async def _remove_menu_childes(db_data: dict, for_delete: list) -> dict:
        """For deleted menus, delete submenus and dishes."""
        deleted_menu = [item.get('id') for item in for_delete]
        db_data['submenus'] = {k: v for k, v in db_data['submenus'].items() if v.get('menu_id') not in deleted_menu}
        db_data['dishes'] = {k: v for k, v in db_data['dishes'].items() if v.get('menu_id') not in deleted_menu}
        return db_data

    @staticmethod
    async def _remove_submenu_childes(db_data: dict, for_delete: list) -> dict:
        """For deleted submenus, delete dishes."""
        deleted_submenu = [item.get('id') for item in for_delete]
        db_data['dishes'] = {k: v for k, v in db_data['dishes'].items() if v.get('submenu_id') not in deleted_submenu}
        return db_data

    @staticmethod
    async def _delete_objects(service: MenuService | SubMenuService | DishService, objects: list):
        """Bulk delete objects."""
        for obj in objects:
            await service.delete(**obj)

    @staticmethod
    async def _find_difference(admin_data: dict, db_data: dict) -> tuple[list, list, list]:
        """Conduct separation objects which need to create, update or delete."""
        for_create = []
        for_update = []
        for_delete = []
        for uid, data in admin_data.items():
            db_object = db_data.get(uid)
            if not db_object:
                for_create.append(data)
            elif db_object != data:
                for_update.append(data)
        for uid, values in db_data.items():
            if not admin_data.get(uid):
                data = {'id': uid}
                if values.get('menu_id'):
                    data['menu_id'] = values.get('menu_id')
                if values.get('submenu_id'):
                    data['submenu_id'] = values.get('submenu_id')
                for_delete.append(data)
        return for_create, for_update, for_delete

    @staticmethod
    async def _parse_db(menus: list) -> dict[str, dict[str, dict]]:
        """
        Parse data to special structure for easy compare.
        Return:
        {
            'menus': {
                '13d81e02-3911-11ee-be56-0242ac120003': {
                    'field_name': 'field_value'
                    ...
                },
                ...
            }
            'submenus': {
                '13d81e02-3911-11ee-be56-0242ac120003': {
                    'field_name': 'field_value'
                    ...
                },
                ...
            }
            'dishes': {
                '13d81e02-3911-11ee-be56-0242ac120003': {
                    'field_name': 'field_value'
                    ...
                },
                ...
            }
        }
        """
        total_menus = {}
        total_submenus = {}
        total_dishes = {}
        for menu in menus:
            total_menus[menu.id] = {
                'id': menu.id,
                'title': menu.title,
                'description': menu.description,
            }
            for submenu in menu.submenus:
                total_submenus[submenu.id] = {
                    'id': submenu.id,
                    'title': submenu.title,
                    'description': submenu.description,
                    'menu_id': menu.id,
                }
                for dish in submenu.dishes:
                    total_dishes[dish.id] = {
                        'id': dish.id,
                        'title': dish.title,
                        'description': dish.description,
                        'price': dish.description,
                        'menu_id': menu.id,
                        'submenu_id': submenu.id,
                    }
        return {'menus': total_menus, 'submenus': total_submenus, 'dishes': total_dishes}


async def get_updater_db() -> UpdaterDB:
    admin_source = settings.ADMIN_GOOGLE_SHEET if settings.FROM_GOOGLE_SHEETS else settings.ADMIN_EXCEL_PATH
    async with async_session_maker() as session:
        cache = await anext(get_redis_connection())
        return UpdaterDB(
            menu_service=MenuService(
                repository=MenuRepository(session=session),
                cache=Cache(redis=cache),
            ),
            submenu_service=SubMenuService(
                repository=SubMenuRepository(session=session),
                cache=Cache(redis=cache),
            ),
            dish_service=DishService(
                repository=DishRepository(session=session),
                cache=Cache(redis=cache),
            ),
            admin_parser=ExcelParser(source=admin_source),
        )
