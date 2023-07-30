import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.submenus.models import SubMenu
from src.dishes.models import Dish


def _select_submenu() -> select:
    """Query for Submenu."""
    dishes_count = select(func.count(Dish.id)).where(
        SubMenu.id == Dish.submenu_id
    )
    return select(
        SubMenu.id,
        SubMenu.title,
        SubMenu.description,
        SubMenu.menu_id,
        dishes_count.label("dishes_count"),
    )


async def get_submenu(
            db: AsyncSession,
            menu_uid: uuid.UUID,
            submenu_uid: uuid.UUID
        ):
    """Get submenu by uid."""
    query = (
        _select_submenu()
        .filter(SubMenu.id == submenu_uid)
        .filter(SubMenu.menu_id == menu_uid)
    )
    obj = await db.execute(query)
    return obj.mappings().first()


async def get_submenus(db: AsyncSession, menu_id: uuid.UUID):
    """Get list of submenus."""
    query = _select_submenu().filter(SubMenu.menu_id == menu_id)
    obj = await db.execute(query)
    return obj.mappings().all()
