import uuid

from fastapi import status
from httpx import AsyncClient

from src.main import app
from src.menus.models import Menu
from src.submenus.models import SubMenu
from tests.conftest import async_test_session_maker
from tests.utils import count_objects, get_object


class TestCrudSubmenus:
    """Тесты для crud операций подменю."""
    async def test_get_submenus(
                self,
                async_client: AsyncClient,
                submenu: SubMenu,
            ):
        """Тест - получение списка подменю."""
        async with async_test_session_maker() as db:
            submenus = await get_object(db=db, model=SubMenu, many=True)
        url = app.url_path_for("get_submenus", menu_id=submenu.menu_id)
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            "Код ответа не корректный"
        )
        assert len(response.json()) == len(submenus), (
            "Выведено неверное количество подменю",
        )
        response_submenu = response.json()[0]
        assert response_submenu.get("id") == str(submenu.id), (
            "У меню отсутствует поле id",
        )
        assert response_submenu.get("title") == submenu.title, (
            "У меню отсутствует поле title",
        )
        assert response_submenu.get("description") == submenu.description, (
            "У меню отсутствует поле description",
        )

    async def test_get_single_submenu(
                self,
                async_client: AsyncClient,
                submenu: SubMenu,
            ):
        """Тест - получение одиночного подменю по id."""
        url = app.url_path_for(
            "get_submenu",
            menu_id=submenu.menu_id,
            submenu_id=submenu.id,
        )
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_200_OK, (
            "Статус код некорректный",
        )
        response_menu = response.json()
        assert response_menu.get("id") == str(submenu.id), "Id отличается"
        assert response_menu.get("title") == submenu.title, "Title отличается"
        assert response_menu.get("description") == submenu.description, (
            "Title отличается",
        )

    async def test_get_non_existing_submenu(
                self,
                async_client: AsyncClient,
                submenu: SubMenu,
            ):
        """Тест - получение несуществующего подменю по id."""
        non_exists_id = uuid.uuid4()
        url = app.url_path_for(
            "get_submenu",
            menu_id=submenu.menu_id,
            submenu_id=non_exists_id,
        )
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            "Если подменю не существует должно отображать ошибку 404",
        )

    async def test_create_submenu(self, async_client: AsyncClient, menu: Menu):
        """Тест - создание подменю."""
        async with async_test_session_maker() as db:
            submenus_count_before = await count_objects(db=db, model=SubMenu)
        submenu_data = {
            "title": "Новое подменю",
            "description": "Описание нового подменю",
        }
        url = app.url_path_for("create_submenu", menu_id=menu.id)
        response = await async_client.post(url, json=submenu_data)
        async with async_test_session_maker() as db:
            submenus_count_after = await count_objects(db=db, model=SubMenu)
        assert response.status_code == status.HTTP_201_CREATED, (
            "Некорректный статус код",
        )
        menu_resp = response.json()
        assert menu_resp.get("title") == submenu_data.get("title"), (
            "Поле title отличается",
        )
        assert menu_resp.get("description") == submenu_data.get("description"), (
            "Поле description отличается",
        )
        assert submenus_count_before + 1 == submenus_count_after, (
            "Количество меню не изменилось",
        )

    async def test_update_submenu(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
            ):
        """Тест - обновление подменю."""
        new_data = {
            "title": "Новый заголовок",
            "description": "Новое описание",
        }
        url = app.url_path_for(
            "update_submenu",
            menu_id=menu.id,
            submenu_id=submenu.id,
        )
        response = await async_client.patch(url, json=new_data)
        data = response.json()
        assert response.status_code == status.HTTP_200_OK, (
            "Некорректный статус код",
        )
        assert data.get("title") == new_data.get("title"), (
            "Поле title отличается",
        )
        assert data.get("description") == new_data.get("description"), (
            "Поле description отличается",
        )
        async with async_test_session_maker() as db:
            updated_submenu = await get_object(
                db=db,
                id=submenu.id,
                model=SubMenu,
            )
        assert updated_submenu.title == new_data.get("title"), (
            "Поле title не изменилось в базе",
        )
        assert updated_submenu.description == new_data.get("description"), (
            "Поле description не изменилось в базе",
        )

    async def test_update_non_exists_submenu(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
            ):
        """Тест - обновление несуществующего подменю."""
        new_data = {
            "title": "Новый заголовок",
            "description": "Новое описание",
        }
        non_exists_id = uuid.uuid4()
        url = app.url_path_for(
            "update_submenu",
            menu_id=menu.id,
            submenu_id=non_exists_id,
        )
        response = await async_client.patch(url, json=new_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            "Если подменю не существует должно отображать ошибку 404",
        )

    async def test_delete_submenu(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
            ):
        """Тест - удалить подменю."""
        url = app.url_path_for(
            "delete_submenu",
            menu_id=menu.id,
            submenu_id=submenu.id,
        )
        response = await async_client.delete(url)
        assert response.status_code == status.HTTP_200_OK, (
            "Некорректный статус код",
        )
        async with async_test_session_maker() as db:
            deleted_submenu = await get_object(
                db=db,
                model=SubMenu,
                id=submenu.id,
            )
        assert deleted_submenu is None, "Подменю не удалилось из базы"

    async def test_delete_non_exist_submenu(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
            ):
        """Тест - удалить несуществующее подменю."""
        non_exists_id = uuid.uuid4()
        url = app.url_path_for(
            "delete_submenu",
            menu_id=menu.id,
            submenu_id=non_exists_id,
        )
        response = await async_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            "Если подменю не существует должно отображать ошибку 404",
        )
