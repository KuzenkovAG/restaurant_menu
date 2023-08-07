from httpx import AsyncClient

from src.dishes.models import Dish
from src.main import app
from src.menus.models import Menu
from src.submenus.models import SubMenu
from tests.conftest import async_test_session_maker
from tests.utils import get_object


class TestCountFields:
    """Тестирование полей отображающих количество блюд и подменю."""

    async def test_menus_count_fields(
        self,
        async_client: AsyncClient,
        menu: Menu,
        submenu: SubMenu,
        two_dishes: list[Dish],
    ):
        """Тест - поля подсчета подменю и блюд при выводе списка меню."""
        url = app.url_path_for('get_menus')
        response = await async_client.get(url)
        response_data = response.json()[0]
        assert response_data.get('submenus_count') == 1, 'Неверное количество подменю'
        assert response_data.get('dishes_count') == 2, 'Неверное количество блюд'

    async def test_submenus_count_fields(
        self,
        async_client: AsyncClient,
        menu: Menu,
        submenu: SubMenu,
        two_dishes: list[Dish],
    ):
        url = app.url_path_for('get_submenus', menu_id=menu.id)
        response = await async_client.get(url)
        response_data = response.json()[0]
        assert response_data.get('dishes_count') == 2, 'Неверное количество блюд'


class TestCascadeDelete:
    """Тестирование каскадного удаления."""

    async def test_cascade_delete_dishes(
        self,
        async_client: AsyncClient,
        menu: Menu,
        submenu: SubMenu,
        two_dishes: list[Dish],
    ):
        """Тест - каскадное удаление блюд."""
        url = app.url_path_for('get_dishes', menu_id=menu.id, submenu_id=submenu.id)
        dishes = await async_client.get(url)
        assert dishes != [], 'В базе нет блюд до удаления'
        url = app.url_path_for('delete_submenu', menu_id=menu.id, submenu_id=submenu.id)
        await async_client.delete(url)
        async with async_test_session_maker() as db:
            dishes = await get_object(db=db, model=Dish, many=True)
        assert dishes == [], 'Блюда не удаляются после удаления подменю.'

    async def test_cascade_delete_submenus(
        self,
        async_client: AsyncClient,
        menu: Menu,
        submenu: SubMenu,
    ):
        """Тест - каскадное удаление блюд."""
        submenus_url = app.url_path_for('get_submenus', menu_id=menu.id)
        submenus = await async_client.get(submenus_url)
        assert submenus != [], 'В базе нет подменю до удаления'
        delete_menu_url = app.url_path_for('delete_menu', menu_id=menu.id)
        await async_client.delete(delete_menu_url)
        async with async_test_session_maker() as db:
            submenus = await get_object(db=db, model=SubMenu, many=True)
        assert submenus == [], 'Подменю не удаляются после удаления меню.'
