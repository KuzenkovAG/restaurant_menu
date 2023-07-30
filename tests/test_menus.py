from typing import List

from fastapi import status
from httpx import AsyncClient

from src.core import crud as crud_core
from src.menus.models import Menu
from src.menus import crud as crud_menu
from .conftest import async_test_session_maker


class TestCrudMenu:
    """Тесты crud операций для меню."""
    async def test_get_menus(
                self,
                async_client: AsyncClient,
                menu: Menu,
            ):
        """Тест - получение списка меню."""
        async with async_test_session_maker() as db:
            menus = await crud_core.get_objects(db=db, model=Menu)
        response = await async_client.get("/api/v1/menus/")
        assert response.status_code == status.HTTP_200_OK, (
            'Код ответа не корректный'
        )
        assert len(response.json()) == len(menus), (
            'Выведено неверное количество меню'
        )
        response_menu = response.json()[0]
        assert response_menu.get('id') is not None, (
            'У меню отсутствует поле id'
        )
        assert response_menu.get('title') is not None, (
            'У меню отсутствует поле title'
        )
        assert response_menu.get('description') is not None, (
            'У меню отсутствует поле description'
        )

    async def test_get_single_menu(
                self,
                async_client: AsyncClient,
                menu: Menu
            ):
        """Тест - получение одиночного меню по id."""
        url = f"/api/v1/menus/{menu.id}"
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            'Статус код некорректный'
        )
        response_menu = response.json()
        assert response_menu.get('id') == str(menu.id), 'Id отличается'
        assert response_menu.get('title') == menu.title, 'Title отличается'
        assert response_menu.get('description') == menu.description, (
            'Title отличается'
        )

    async def test_create_menu(self, async_client: AsyncClient):
        """Тест - создание меню."""
        async with async_test_session_maker() as db:
            menus_count_before = await crud_core.count_objects(
                db=db,
                model=Menu
            )
        menu_data = {
            "title": "Напитки",
            "description": "Меню с напитками"
        }
        response = await async_client.post("/api/v1/menus/", json=menu_data)
        async with async_test_session_maker() as db:
            menus_count_after = await crud_core.count_objects(
                db=db,
                model=Menu
            )
        assert response.status_code == status.HTTP_201_CREATED, (
            'Некорректный статус код'
        )
        menu = response.json()
        assert menu.get('title') == menu_data.get('title'), (
            'Поле title отличается'
        )
        assert menu.get('description') == menu_data.get('description'), (
            'Поле description отличается'
        )
        assert menus_count_before + 1 == menus_count_after, (
            'Количество меню не изменилось'
        )

    async def test_update_menu(self, async_client: AsyncClient, menu: Menu):
        """Тест - обновление меню"""
        new_data = {
            "title": "Новый заголовок",
            "description": "Новое описание"
        }
        url = f"/api/v1/menus/{menu.id}"
        response = await async_client.patch(url, json=new_data)
        response_menu = response.json()
        assert response.status_code == status.HTTP_200_OK, (
            'Некорректный статус код'
        )
        assert response_menu.get('title') == new_data.get('title'), (
            'Поле title отличается'
        )
        assert response_menu.get('description') == new_data.get('description'), (
            'Поле description отличается'
        )
        async with async_test_session_maker() as db:
            updated_menu = await crud_menu.get_menu(db=db, uid=menu.id)
        assert updated_menu.title == new_data.get('title'), (
            'Поле title не изменилось в базе'
        )
        assert updated_menu.description == new_data.get('description'), (
            'Поле description не изменилось в базе'
        )

    async def test_delete_menu(self, async_client: AsyncClient, menu: Menu):
        """Тест - удалить меню."""
        async with async_test_session_maker() as db:
            menus_count_before = await crud_core.count_objects(
                db=db,
                model=Menu
            )
        url = f"/api/v1/menus/{menu.id}"
        response = await async_client.delete(url)
        assert response.status_code == status.HTTP_200_OK, (
            'Некорректный статус код'
        )
        async with async_test_session_maker() as db:
            deleted_menu = await crud_menu.get_menu(db=db, uid=menu.id)
        assert deleted_menu is None, (
            'Меню не удалилось из базы'
        )
        async with async_test_session_maker() as db:
            menus_count_after = await crud_core.count_objects(
                db=db,
                model=Menu
            )
        assert menus_count_before == menus_count_after + 1, (
            'Количество меню в базе не изменилось'
        )
