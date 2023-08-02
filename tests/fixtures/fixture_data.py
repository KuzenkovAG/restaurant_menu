import pytest

from tests.conftest import async_test_session_maker

from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept
from src.core.crud import bulk_create, create_object
from src.dishes.models import Dish
from src.menus.models import Menu
from src.submenus.models import SubMenu


menu_data = {
    "title": "Тестовое меню",
    "description": "Меню для теста"
}
submenu_data = {
    "title": "Тестовое подменю",
    "description": "Подменю для теста"
}
dish_data = {
    "title": "Тестовое блюдо",
    "description": "Блюдо для теста",
    "price": 1.23
}


@pytest.fixture
async def menu() -> DeclarativeAttributeIntercept:
    """Создание меню."""
    async with async_test_session_maker() as db:
        menu = await create_object(db=db, data=menu_data, model=Menu)
        return menu


@pytest.fixture
async def submenu(menu: Menu) -> DeclarativeAttributeIntercept:
    """Создание подменю."""
    submenu_data['menu_id'] = menu.id
    async with async_test_session_maker() as db:
        submenu = await create_object(db=db, data=submenu_data, model=SubMenu)
        return submenu


@pytest.fixture
async def dish(submenu: SubMenu) -> DeclarativeAttributeIntercept:
    """Создание блюда."""
    dish_data['submenu_id'] = submenu.id
    async with async_test_session_maker() as db:
        dish = await create_object(db=db, data=dish_data, model=Dish)
        return dish


@pytest.fixture
async def two_dishes(submenu: SubMenu) -> DeclarativeAttributeIntercept:
    """Создание нескольких блюд."""
    dish_data['submenu_id'] = submenu.id
    async with async_test_session_maker() as db:
        datas = [dish_data for _ in range(2)]
        dishes = await bulk_create(db=db, datas=datas, model=Dish)
        return dishes
