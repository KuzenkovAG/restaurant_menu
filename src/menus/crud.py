import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.menus import models
from src.submenus.models import SubMenu
from src.dishes.models import Dish


def _select_menu() -> select:
    """Query for Menu."""
    submenus_count = select(func.count(SubMenu.id)).where(
        SubMenu.menu_id == models.Menu.id
    )
    dishes_count = select(func.count(Dish.id)).where(
        SubMenu.menu_id == models.Menu.id
    ).where(Dish.submenu_id == SubMenu.id)
    return select(
        models.Menu.id,
        models.Menu.title,
        models.Menu.description,
        submenus_count.label("submenus_count"),
        dishes_count.label("dishes_count"),
    )


async def get_menu(db: AsyncSession, uid: uuid.UUID):
    """Get menu by uid."""
    query = _select_menu().filter(models.Menu.id == uid)
    obj = await db.execute(query)
    return obj.mappings().first()


async def get_menus(db: AsyncSession):
    """Get list of menus."""
    query = _select_menu()
    obj = await db.execute(query)
    return obj.mappings().all()
