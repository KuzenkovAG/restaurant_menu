import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.menus import models


async def get_menu(db: AsyncSession, uid: uuid.UUID):
    """Get menu by uid."""
    query = select(models.Menu).filter(models.Menu.id == uid)
    obj = await db.execute(query)
    return obj.scalars().first()


async def get_menus(db: AsyncSession):
    """Get list of menus."""
    query = select(models.Menu)
    obj = await db.execute(query)
    return obj.scalars().all()
