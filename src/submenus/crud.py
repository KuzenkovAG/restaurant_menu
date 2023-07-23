import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.submenus import models, schemas


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


async def get_submenu_by_tutle(db: AsyncSession, title: str):
    """Get submenu by title."""
    query = select(models.SubMenu).filter(models.SubMenu.title == title)
    obj = await db.execute(query)
    return obj.scalars().first()


async def get_submenus(db: AsyncSession, menu_id: uuid.UUID):
    """Get list of submenus."""
    query = select(models.SubMenu).filter(models.SubMenu.menu_id == menu_id)
    obj = await db.execute(query)
    return obj.scalars().all()


async def create_submenu(
            db: AsyncSession,
            data: schemas.SubMenuCreationInput,
            menu_id: uuid.UUID
        ):
    """Create submenu."""
    data = data.dict()
    data['menu_id'] = menu_id
    created_object = models.SubMenu(**data)
    db.add(created_object)
    await db.commit()
    return created_object


async def update_submenu(
            db: AsyncSession,
            updated_data: schemas.SubMenuCreationInput,
            submenu: schemas.SubMenuCreationInput
        ):
    """Update submenu."""
    for field, value in updated_data.dict().items():
        setattr(submenu, field, value)
    db.add(submenu)
    await db.commit()
    await db.refresh(submenu)
    return submenu


async def delete_submenu(db: AsyncSession, submenu: schemas.SubMenu):
    """Delete submenu."""
    await db.delete(submenu)
    await db.commit()
