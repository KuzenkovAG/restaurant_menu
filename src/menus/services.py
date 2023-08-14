import uuid
from typing import Annotated

from fastapi import BackgroundTasks, Depends

from src.core.cashe import Cache, get_cache
from src.menus import schemas
from src.menus.repositories import MenuRepository, get_menu_repository


class MenuService:
    """Service for Menu."""

    def __init__(
            self,
            repository: MenuRepository,
            cache: Cache,
            background_tasks: BackgroundTasks = BackgroundTasks(),
    ):
        self.repository = repository
        self.cache = cache
        self.background_tasks = background_tasks

    async def get(self, **filters: uuid.UUID | str) -> schemas.Menu:
        """Get menu with filters."""
        key = f"menu_{filters.get('id')}"
        menu_cache = await self.cache.get(key)
        if menu_cache:
            return schemas.Menu.model_validate(menu_cache)
        menu = await self.repository.get_object_or_404(**filters)
        await self.cache.set(key, menu)
        return menu

    async def get_all(self) -> list[schemas.Menu]:
        """Get all menus."""
        key = 'menus'
        menus_cache = await self.cache.get(key=key)
        if menus_cache:
            return [schemas.Menu.model_validate(menu) for menu in menus_cache]
        menus = await self.repository.get_all()
        await self.cache.set(key=key, value=menus)
        return menus

    async def get_with_relations(self) -> list[schemas.MenuWithRelations]:
        """Get menus with relations."""
        key = 'menus_relations'
        cache = await self.cache.get(key=key)
        if cache:
            return [schemas.MenuWithRelations.model_validate(menu) for menu in cache]
        menus = await self.repository.get_with_relations()
        menus_with_relations = [schemas.MenuWithRelations.model_validate(menu[0]) for menu in menus]
        await self.cache.set(key=key, value=menus_with_relations)
        return menus_with_relations

    async def create(self, data: schemas.MenuCreateInput, **kwargs: uuid.UUID | str) -> schemas.MenuCreateOutput:
        """Create menu."""
        menu = await self.repository.create(data=data, **kwargs)
        self.background_tasks.add_task(self.cache.clear, 'menus', 'menus_relations')
        return schemas.MenuCreateOutput.model_validate(menu)

    async def update(self, data: schemas.MenuCreateInput, menu_id: uuid.UUID | str) -> schemas.MenuCreateOutput:
        """Update menu."""
        menu = await self.repository.update(id=menu_id, data=data)
        self.background_tasks.add_task(self.cache.clear, 'menus', 'menus_relations', f'menu_{menu_id}')
        return schemas.MenuCreateOutput.model_validate(menu)

    async def delete(self, id: uuid.UUID) -> None:
        """Delete menu."""
        await self.repository.delete(id=id)
        self.background_tasks.add_task(self.cache.clear, 'menus', 'menus_relations')
        self.background_tasks.add_task(self.cache.clear_by_mask, f'menu_{id}')


async def get_menu_service(
    background_tasks: BackgroundTasks,
    repository: Annotated[MenuRepository, Depends(get_menu_repository)],
    cache: Annotated[Cache, Depends(get_cache)],
) -> MenuService:
    return MenuService(repository=repository, cache=cache, background_tasks=background_tasks)
