from typing import List

from fastapi import status
from httpx import AsyncClient

from src.core import crud as crud_core
from src.dishes.models import Dish
from src.dishes import crud as crud_dish
from src.menus.models import Menu
from src.submenus.models import SubMenu
from .conftest import async_test_session_maker


class TestCrudDishes:
    """Тесты для crud операций блюд."""
    async def test_get_dishes(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                dish: Dish,
            ):
        """Тест - получение списка блюд."""
        async with async_test_session_maker() as db:
            dishes = await crud_core.get_objects(db=db, model=Dish)
        url = f'/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/'
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            'Код ответа не корректный'
        )
        assert len(response.json()) == len(dishes), (
            'Выведено неверное количество блюд'
        )
        response_data = response.json()[0]
        assert response_data.get('id') is not None, (
            'У меню отсутствует поле id'
        )
        assert response_data.get('title') is not None, (
            'У меню отсутствует поле title'
        )
        assert response_data.get('description') is not None, (
            'У меню отсутствует поле description'
        )
        assert response_data.get('price') is not None, (
            'У меню отсутствует поле price'
        )

    async def test_get_single_dish(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                dish: Dish
            ):
        """Тест - получение одиночного блюда по id."""
        url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            'Статус код некорректный'
        )
        response_data = response.json()
        assert response_data.get('id') == str(dish.id), 'Id отличается'
        assert response_data.get('title') == dish.title, 'Title отличается'
        assert response_data.get('description') == dish.description, (
            'Title отличается'
        )
        assert response_data.get('price') == str(dish.price), (
            'Price отличается'
        )

    async def test_create_dish(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
            ):
        """Тест - создание блюда."""
        async with async_test_session_maker() as db:
            dishes_count_before = await crud_core.count_objects(
                db=db,
                model=Dish
            )
        dish_data = {
            "title": "Новое блюдо",
            "description": "Описание нового блюда",
            "price": "1.23"
        }
        url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/"
        response = await async_client.post(url, json=dish_data)
        async with async_test_session_maker() as db:
            dishes_count_after = await crud_core.count_objects(
                db=db,
                model=Dish
            )
        assert response.status_code == status.HTTP_201_CREATED, (
            'Некорректный статус код'
        )
        data = response.json()
        assert data.get('title') == dish_data.get('title'), (
            'Поле title отличается'
        )
        assert data.get('description') == dish_data.get('description'), (
            'Поле description отличается'
        )
        assert data.get('price') == dish_data.get('price'), (
            'Поле description отличается'
        )
        assert dishes_count_before + 1 == dishes_count_after, (
            'Количество меню не изменилось'
        )

    async def test_update_dish(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                dish: Dish
            ):
        """Тест - обновление подменю."""
        new_data = {
            "title": "Новый заголовок",
            "description": "Новое описание",
            "price": "3.21"
        }
        url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
        response = await async_client.patch(url, json=new_data)
        data = response.json()
        assert response.status_code == status.HTTP_200_OK, (
            'Некорректный статус код'
        )
        assert data.get('title') == new_data.get('title'), (
            'Поле title отличается'
        )
        assert data.get('description') == new_data.get('description'), (
            'Поле description отличается'
        )
        assert data.get('price') == new_data.get('price'), (
            'Поле price отличается'
        )
        async with async_test_session_maker() as db:
            updated_dish = await crud_dish.get_dish(
                db=db,
                dish_uid=dish.id,
                submenu_uid=submenu.id
            )
        assert updated_dish.title == new_data.get('title'), (
            'Поле title не изменилось в базе'
        )
        assert updated_dish.description == new_data.get('description'), (
            'Поле description не изменилось в базе'
        )
        assert str(updated_dish.price) == new_data.get('price'), (
            'Поле price не изменилось в базе'
        )

    async def test_delete_dish(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                dish: Dish
            ):
        """Тест - удалить блюдо."""
        async with async_test_session_maker() as db:
            dishes_count_before = await crud_core.count_objects(
                db=db,
                model=Dish
            )
        url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
        response = await async_client.delete(url)
        assert response.status_code == status.HTTP_200_OK, (
            'Некорректный статус код'
        )
        async with async_test_session_maker() as db:
            deleted_dish = await crud_dish.get_dish(
                db=db,
                dish_uid=dish.id,
                submenu_uid=submenu.id
            )
        assert deleted_dish is None, (
            'Блюдо не удалилось из базы'
        )
        async with async_test_session_maker() as db:
            submenus_count_after = await crud_core.count_objects(
                db=db,
                model=Dish
            )
        assert dishes_count_before == submenus_count_after + 1, (
            'Количество блюд в базе не изменилось'
        )
