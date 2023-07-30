from typing import List

from httpx import AsyncClient

from src.core import crud as crud_core
from src.dishes.models import Dish
from src.menus.models import Menu
from src.submenus.models import SubMenu
from .conftest import async_test_session_maker


class TestCountFields:
    """Тестирование полей отображающих количество блюд и подменю."""
    async def test_menus_count_fields(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                two_dishes: List[Dish],
            ):
        """Тест - поля подсчета подменю и блюд при выводе списка меню."""
        response = await async_client.get("/api/v1/menus/")
        response_data = response.json()[0]
        assert response_data.get('submenus_count') == 1, (
            'Неверное количество подменю'
        )
        assert response_data.get('dishes_count') == 2, (
            'Неверное количество блюд'
        )

    async def test_submenus_count_fields(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                two_dishes: List[Dish],
            ):
        url = f"/api/v1/menus/{menu.id}/submenus/"
        response = await async_client.get(url)
        response_data = response.json()[0]
        assert response_data.get('dishes_count') == 2, (
            'Неверное количество блюд'
        )


class TestCascadeDelete:
    """Тестирование каскадного удаления."""
    async def test_cascade_delete_dishes(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                two_dishes: List[Dish],
            ):
        """Тест - каскадное удаление блюд."""
        submenus_url = f"/api/v1/menus/{menu.id}/submenus/"
        dishes = await async_client.get(submenus_url)
        assert dishes != [], 'В базе нет блюд до удаления'
        url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}"
        await async_client.delete(url)
        async with async_test_session_maker() as db:
            dishes = await crud_core.get_objects(
                db=db,
                model=Dish
            )
        assert dishes == [], 'Блюда не удаляются после удаления подменю.'

    async def test_cascade_delete_submenus(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
            ):
        """Тест - каскадное удаление блюд."""
        submenus_url = f"/api/v1/menus/{menu.id}/submenus/"
        submenus = await async_client.get(submenus_url)
        assert submenus != [], 'В базе нет подменю до удаления'
        delete_menu_url = f"/api/v1/menus/{menu.id}"
        await async_client.delete(delete_menu_url)
        async with async_test_session_maker() as db:
            submenus = await crud_core.get_objects(
                db=db,
                model=SubMenu
            )
        assert submenus == [], 'Подменю не удаляются после удаления меню.'
