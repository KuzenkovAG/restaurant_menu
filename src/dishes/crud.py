import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dishes import models


async def get_dish(
            db: AsyncSession,
            submenu_uid: uuid.UUID,
            dish_uid: uuid.UUID
        ):
    """Get dish by uid."""
    query = (
        select(models.Dish)
        .filter(models.Dish.id == dish_uid)
        .filter(models.Dish.submenu_id == submenu_uid)
    )
    obj = await db.execute(query)
    return obj.scalars().first()


async def get_dishes(db: AsyncSession, submenu_id: uuid.UUID):
    """Get list of dishes."""
    query = select(models.Dish).filter(models.Dish.submenu_id == submenu_id)
    obj = await db.execute(query)
    return obj.scalars().all()
