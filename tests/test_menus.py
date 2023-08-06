import uuid

from fastapi import status
from httpx import AsyncClient

from src.main import app
from src.menus.models import Menu
from tests.conftest import async_test_session_maker
from tests.utils import count_objects, get_object


class TestCrudMenu:
    """Тесты crud операций для меню."""
    async def test_get_menus(
                self,
                async_client: AsyncClient,
                menu: Menu,
            ):
        """Тест - получение списка меню."""
        async with async_test_session_maker() as db:
            menus = await get_object(db=db, model=Menu, many=True)
        url = app.url_path_for("get_menus")
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_200_OK, "Код ответа не корректный"
        assert len(response.json()) == len(menus), "Выведено неверное количество меню"
        response_menu = response.json()[0]
        assert response_menu.get("id") == str(menu.id), "Поле id отличается"
        assert response_menu.get("title") == menu.title, "Поле title отличается"
        assert response_menu.get("description") == menu.description, (
            "Поле description отличается",
        )

    async def test_get_single_menu(self, async_client: AsyncClient, menu: Menu):
        """Тест - получение одиночного меню по id."""
        url = app.url_path_for("get_menu", menu_id=menu.id)
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_200_OK, "Статус код некорректный"
        response_menu = response.json()
        assert response_menu.get("id") == str(menu.id), "Id отличается"
        assert response_menu.get("title") == menu.title, "Title отличается"
        assert response_menu.get("description") == menu.description, "Title отличается"

    async def test_get_non_existent_menu(self, async_client: AsyncClient, menu: Menu):
        """Тест - получение несуществующего меню."""
        non_existent_id = uuid.uuid4()
        url = app.url_path_for("get_menu", menu_id=non_existent_id)
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            "Если меню не существует, должно отображать ошибку 404",
        )

    async def test_create_menu(self, async_client: AsyncClient):
        """Тест - создание меню."""
        async with async_test_session_maker() as db:
            menus_count_before = await count_objects(db=db, model=Menu)
        menu_data = {
            "title": "Напитки",
            "description": "Меню с напитками",
        }
        url = app.url_path_for("create_menu")
        response = await async_client.post(url, json=menu_data)
        async with async_test_session_maker() as db:
            menus_count_after = await count_objects(db=db, model=Menu)
        assert response.status_code == status.HTTP_201_CREATED, (
            "Некорректный статус код",
        )
        menu = response.json()
        assert menu.get("title") == menu_data.get("title"), (
            "Поле title отличается",
        )
        assert menu.get("description") == menu_data.get("description"), (
            "Поле description отличается",
        )
        assert menus_count_before + 1 == menus_count_after, (
            "Количество меню не изменилось",
        )
        async with async_test_session_maker() as db:
            created_menu = await get_object(db=db, model=Menu, id=menu.get("id"))
        assert created_menu.title == menu_data.get("title"), (
            "Поле title отличается в базе",
        )
        assert created_menu.description == menu_data.get("description"), (
            "Поле description отличается в базе",
        )

    async def test_update_menu(self, async_client: AsyncClient, menu: Menu):
        """Тест - обновление меню"""
        new_data = {
            "title": "Новый заголовок",
            "description": "Новое описание",
        }
        url = app.url_path_for("update_menu", menu_id=menu.id)
        response = await async_client.patch(url, json=new_data)
        data = response.json()
        assert response.status_code == status.HTTP_200_OK, "Некорректный статус код"
        assert data.get("title") == new_data.get("title"), "Поле title отличается"
        assert data.get("description") == new_data.get("description"), (
            "Поле description отличается",
        )
        async with async_test_session_maker() as db:
            updated_menu = await get_object(db=db, model=Menu, id=menu.id)
        assert updated_menu.title == new_data.get("title"), (
            "Поле title не изменилось в базе",
        )
        assert updated_menu.description == new_data.get("description"), (
            "Поле description не изменилось в базе",
        )

    async def test_update_non_exist_menu(
                self,
                async_client: AsyncClient,
                menu: Menu,
            ):
        """Тест - обновить несуществующее подменю."""
        new_data = {
            "title": "Новый заголовок",
            "description": "Новое описание",
        }
        non_exists_id = uuid.uuid4()
        url = app.url_path_for("update_menu", menu_id=non_exists_id)
        response = await async_client.patch(url, json=new_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            "Если меню не существует, должно отображать ошибку 404",
        )

    async def test_delete_menu(self, async_client: AsyncClient, menu: Menu):
        """Тест - удалить меню."""
        async with async_test_session_maker() as db:
            menu_for_delete = await get_object(db=db, model=Menu, id=menu.id)
        assert menu_for_delete is not None, "Удаляемого меню нет в базе"
        url = app.url_path_for("delete_menu", menu_id=menu.id)
        response = await async_client.delete(url)
        assert response.status_code == status.HTTP_200_OK, (
            "Некорректный статус код",
        )
        async with async_test_session_maker() as db:
            deleted_menu = await get_object(db=db, model=Menu, id=menu.id)
        assert deleted_menu is None, "Меню не удалилось из базы"

    async def test_delete_non_exist_menu(
                self,
                async_client: AsyncClient,
                menu: Menu,
            ):
        """Тест - удалить несуществующее подменю."""
        non_exists_id = uuid.uuid4()
        url = app.url_path_for("delete_menu", menu_id=non_exists_id)
        response = await async_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            "Если меню не существует, должно отображать ошибку 404",
        )
