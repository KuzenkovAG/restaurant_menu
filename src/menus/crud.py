import uuid

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.menus import models, schemas


async def get_menu(db: AsyncSession, uid: uuid.UUID):
    """Get menu by uid."""
    query = select(models.Menu).filter(models.Menu.id == uid)
    obj = await db.execute(query)
    return obj.scalars().first()


async def get_menu_by_tutle(db: AsyncSession, title: str):
    """Get menu by title."""
    query = select(models.Menu).filter(models.Menu.title == title)
    obj = await db.execute(query)
    return obj.scalars().first()


async def get_menus(db: AsyncSession):
    """Get list of menus."""
    query = select(models.Menu)
    obj = await db.execute(query)
    return obj.scalars().all()


async def create_menu(db: AsyncSession, data: BaseModel):
    """Create object."""
    created_object = models.Menu(**data.dict())
    db.add(created_object)
    await db.commit()
    return created_object


async def update_menu(
            db: AsyncSession,
            updated_data: schemas.MenuCreateInput,
            menu: schemas.MenuCreateOutput
        ):
    """Update menu."""
    for field, value in updated_data.dict().items():
        setattr(menu, field, value)
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return menu


async def delete_menu(db: AsyncSession, menu: schemas.Menu):
    """Delete object."""
    await db.delete(menu)
    await db.commit()
