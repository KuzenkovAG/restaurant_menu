from typing import List

import pytest
from fastapi import status
from httpx import AsyncClient

from src.core import crud as crud_core
from src.menus.models import Menu
from src.submenus.models import SubMenu
from src.submenus import crud as crud_submenu
from .conftest import async_test_session_maker


class TestCrudSubmenus:
    """Тесты для crud операций подменю."""
    async def test_get_submenus(
                self,
                async_client: AsyncClient,
                submenu: SubMenu,
            ):
        """Тест - получение списка подменю."""
        async with async_test_session_maker() as db:
            submenus = await crud_core.get_objects(db=db, model=SubMenu)
        url = f'/api/v1/menus/{submenu.menu_id}/submenus/'
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            'Код ответа не корректный'
        )
        assert len(response.json()) == len(submenus), (
            'Выведено неверное количество подменю'
        )
        response_submenu = response.json()[0]
        assert response_submenu.get('id') is not None, (
            'У меню отсутствует поле id'
        )
        assert response_submenu.get('title') is not None, (
            'У меню отсутствует поле title'
        )
        assert response_submenu.get('description') is not None, (
            'У меню отсутствует поле description'
        )

    async def test_get_single_submenu(
                self,
                async_client: AsyncClient,
                submenu: SubMenu
            ):
        """Тест - получение одиночного подменю по id."""
        url = f"/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}"
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            'Статус код некорректный'
        )
        response_menu = response.json()
        assert response_menu.get('id') == str(submenu.id), 'Id отличается'
        assert response_menu.get('title') == submenu.title, 'Title отличается'
        assert response_menu.get('description') == submenu.description, (
            'Title отличается'
        )

    async def test_create_submenu(
                self,
                async_client: AsyncClient,
                menu: Menu
            ):
        """Тест - создание подменю."""
        async with async_test_session_maker() as db:
            submenus_count_before = await crud_core.count_objects(
                db=db,
                model=SubMenu
            )
        submenu_data = {
            "title": "Новое подменю",
            "description": "Описание нового подменю"
        }
        url = f"/api/v1/menus/{menu.id}/submenus/"
        response = await async_client.post(url, json=submenu_data)
        async with async_test_session_maker() as db:
            submenus_count_after = await crud_core.count_objects(
                db=db,
                model=SubMenu
            )
        assert response.status_code == status.HTTP_201_CREATED, (
            'Некорректный статус код'
        )
        menu = response.json()
        assert menu.get('title') == submenu_data.get('title'), (
            'Поле title отличается'
        )
        assert menu.get('description') == submenu_data.get('description'), (
            'Поле description отличается'
        )
        assert submenus_count_before + 1 == submenus_count_after, (
            'Количество меню не изменилось'
        )

    async def test_update_submenu(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu
            ):
        """Тест - обновление подменю."""
        new_data = {
            "title": "Новый заголовок",
            "description": "Новое описание"
        }
        url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}"
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
        async with async_test_session_maker() as db:
            updated_submenu = await crud_core.get_object(
                db=db,
                uid=submenu.id,
                model=SubMenu
            )
        assert updated_submenu.title == new_data.get('title'), (
            'Поле title не изменилось в базе'
        )
        assert updated_submenu.description == new_data.get('description'), (
            'Поле description не изменилось в базе'
        )

    async def test_delete_submenu(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu
            ):
        """Тест - удалить подменю."""
        async with async_test_session_maker() as db:
            submenus_count_before = await crud_core.count_objects(
                db=db,
                model=SubMenu
            )
        url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}"
        response = await async_client.delete(url)
        assert response.status_code == status.HTTP_200_OK, (
            'Некорректный статус код'
        )
        async with async_test_session_maker() as db:
            deleted_submenu = await crud_submenu.get_submenu(
                db=db,
                menu_uid=menu.id,
                submenu_uid=submenu.id
            )
        assert deleted_submenu is None, (
            'Подменю не удалилось из базы'
        )
        async with async_test_session_maker() as db:
            submenus_count_after = await crud_core.count_objects(
                db=db,
                model=SubMenu
            )
        assert submenus_count_before == submenus_count_after + 1, (
            'Количество подменю в базе не изменилось'
        )
