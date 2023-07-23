import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dishes import models, schemas


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


async def get_dish_by_title(db: AsyncSession, title: str):
    """Get dish by title."""
    query = select(models.Dish).filter(models.Dish.title == title)
    obj = await db.execute(query)
    return obj.scalars().first()


async def get_dishes(db: AsyncSession, submenu_id: uuid.UUID):
    """Get list of dishes."""
    query = select(models.Dish).filter(models.Dish.submenu_id == submenu_id)
    obj = await db.execute(query)
    return obj.scalars().all()


async def create_dish(
            db: AsyncSession,
            data: schemas.CreateDish,
            submenu_id: uuid.UUID
        ):
    """Create dish."""
    data = data.dict()
    data['submenu_id'] = submenu_id
    created_object = models.Dish(**data)
    db.add(created_object)
    await db.commit()
    return created_object


async def update_dish(
            db: AsyncSession,
            updated_data: schemas.CreateDish,
            dish: schemas.Dish
        ):
    """Update dish."""
    for field, value in updated_data.dict().items():
        setattr(dish, field, value)
    db.add(dish)
    await db.commit()
    await db.refresh(dish)
    return dish


async def delete_dish(db: AsyncSession, dish: schemas.Dish):
    """Delete dish."""
    await db.delete(dish)
    await db.commit()
