import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.submenus import models


async def get_submenu(
            db: AsyncSession,
            menu_uid: uuid.UUID,
            submenu_uid: uuid.UUID
        ):
    """Get submenu by uid."""
    query = (
        select(models.SubMenu)
        .filter(models.SubMenu.id == submenu_uid)
        .filter(models.SubMenu.menu_id == menu_uid)
    )
    obj = await db.execute(query)
    return obj.scalars().first()


async def get_submenus(db: AsyncSession, menu_id: uuid.UUID):
    """Get list of submenus."""
    query = select(models.SubMenu).filter(models.SubMenu.menu_id == menu_id)
    obj = await db.execute(query)
    return obj.scalars().all()
