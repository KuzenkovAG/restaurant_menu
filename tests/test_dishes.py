import uuid

from fastapi import status
from httpx import AsyncClient

from src.dishes.models import Dish
from src.main import app
from src.menus.models import Menu
from src.submenus.models import SubMenu
from tests.conftest import async_test_session_maker
from tests.utils import get_object


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
            dishes = await get_object(
                db=db, model=Dish, many=True, submenu_id=submenu.id,
            )
        url = app.url_path_for(
            "get_dishes",
            menu_id=submenu.menu_id,
            submenu_id=submenu.id,
        )
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_200_OK, "Код ответа не корректный"
        assert len(response.json()) == len(dishes), "Выведено неверное количество блюд"
        response_data = response.json()[0]
        assert response_data.get("id") == str(dish.id), "У блюда некорректное поле id"
        assert response_data.get("title") == dish.title, (
            "У блюда некорректное поле title"
        )
        assert response_data.get("description") == dish.description, (
            "У блюда некорректное поле description"
        )
        assert response_data.get("price") == str(dish.price), (
            "У блюда некорректное поле price"
        )

    async def test_get_single_dish(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                dish: Dish,
            ):
        """Тест - получение блюда по id."""
        url = app.url_path_for(
            "get_dish",
            menu_id=submenu.menu_id,
            submenu_id=submenu.id,
            dish_id=dish.id,
        )
        response = await async_client.get(url)
        assert response.status_code == status.HTTP_200_OK, "Статус код некорректный"
        response_data = response.json()
        assert response_data.get("id") == str(dish.id), "Id отличается"
        assert response_data.get("title") == dish.title, "Title отличается"
        assert response_data.get("description") == dish.description, (
            "Description отличается"
        )
        assert response_data.get("price") == str(dish.price), "Price отличается"

    async def test_get_non_existed_dish(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                dish: Dish,
            ):
        """Тест - получение несуществующего блюда по id."""
        non_existed_id = uuid.uuid4()
        url = app.url_path_for(
            "get_dish",
            menu_id=submenu.menu_id,
            submenu_id=submenu.id,
            dish_id=non_existed_id,
        )
        response = await async_client.get(url)
        assert (response.status_code == status.HTTP_404_NOT_FOUND), (
            "Если блюда не существует, должно отображать ошибку 404"
        )

    async def test_create_dish(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
            ):
        """Тест - создание блюда."""
        dish_data = {
            "title": "Новое блюдо",
            "description": "Описание нового блюда",
            "price": "1.23",
        }
        url = app.url_path_for(
            "create_dish",
            menu_id=menu.id,
            submenu_id=submenu.id,
        )
        response = await async_client.post(url, json=dish_data)
        assert response.status_code == status.HTTP_201_CREATED, (
            "Некорректный статус код"
        )
        data = response.json()
        assert data.get("title") == dish_data.get("title"), "Поле title отличается"
        assert data.get("description") == dish_data.get("description"), (
            "Поле description отличается"
        )
        assert data.get("price") == dish_data.get("price"), (
            "Поле description отличается"
        )
        async with async_test_session_maker() as db:
            created_dish = await get_object(db=db, model=Dish, id=data.get("id"))
        assert created_dish.title == dish_data.get("title"), "Поле title отличается"
        assert created_dish.description == dish_data.get("description"), (
            "Поле description отличается"
        )
        assert str(created_dish.price) == dish_data.get("price"), (
            "Поле description отличается"
        )

    async def test_update_dish(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                dish: Dish,
            ):
        """Тест - обновление подменю."""
        new_data = {
            "title": "Новый заголовок",
            "description": "Новое описание",
            "price": "3.21",
        }
        url = app.url_path_for(
            "update_dish",
            menu_id=submenu.menu_id,
            submenu_id=submenu.id,
            dish_id=dish.id,
        )
        response = await async_client.patch(url, json=new_data)
        data = response.json()
        assert response.status_code == status.HTTP_200_OK, "Некорректный статус код"
        assert data.get("title") == new_data.get("title"), "Поле title отличается"
        assert data.get("description") == new_data.get("description"), (
            "Поле description отличается"
        )
        assert data.get("price") == new_data.get("price"), "Поле price отличается"
        async with async_test_session_maker() as db:
            updated_dish = await get_object(
                db=db,
                model=Dish,
                id=dish.id,
                submenu_id=submenu.id,
            )
        assert updated_dish.title == new_data.get("title"), (
            "Поле title не изменилось в базе"
        )
        assert updated_dish.description == new_data.get("description"), (
            "Поле description не изменилось в базе"
        )
        assert str(updated_dish.price) == new_data.get("price"), (
            "Поле price не изменилось в базе"
        )

    async def test_update_non_existed_dish(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                dish: Dish,
            ):
        """Тест - обновление несуществующего блюда по id."""
        non_existed_id = uuid.uuid4()
        url = app.url_path_for(
            "update_dish",
            menu_id=submenu.menu_id,
            submenu_id=submenu.id,
            dish_id=non_existed_id,
        )
        data = {
            "title": "Новый заголовок",
            "description": "Новое описание",
            "price": "3.21",
        }
        response = await async_client.patch(url, json=data)
        assert (
            response.status_code == status.HTTP_404_NOT_FOUND
        ), "Если блюда не существует, должно отображать ошибку 404"

    async def test_delete_dish(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                dish: Dish,
            ):
        """Тест - удалить блюдо."""
        url = app.url_path_for(
            "delete_dish",
            menu_id=submenu.menu_id,
            submenu_id=submenu.id,
            dish_id=dish.id,
        )
        response = await async_client.delete(url)
        assert response.status_code == status.HTTP_200_OK, "Некорректный статус код"
        async with async_test_session_maker() as db:
            deleted_dish = await get_object(
                db=db,
                model=Dish,
                id=dish.id,
                submenu_id=submenu.id,
            )
        assert deleted_dish is None, "Блюдо не удалилось из базы"

    async def test_delete_non_existed_dish(
                self,
                async_client: AsyncClient,
                menu: Menu,
                submenu: SubMenu,
                dish: Dish,
            ):
        """Тест - удаления несуществующего блюда по id."""
        non_existed_id = uuid.uuid4()
        url = app.url_path_for(
            "delete_dish",
            menu_id=submenu.menu_id,
            submenu_id=submenu.id,
            dish_id=non_existed_id,
        )
        response = await async_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND, (
            "Если блюда не существует, должно отображать ошибку 404"
        )
