from typing import Dict

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base


async def get_object_by_title(db: AsyncSession, title: str, model: Base):
    """Get object by title."""
    query = select(model).filter(model.title == title)
    obj = await db.execute(query)
    return obj.scalars().first()


async def create_object(
            db: AsyncSession,
            data: Dict,
            model: Base
        ):
    """Create object."""
    created_object = model(**data)
    db.add(created_object)
    await db.commit()
    return created_object


async def update_object(
            db: AsyncSession,
            updated_data: BaseModel,
            obj: BaseModel
        ):
    """Update object."""
    for field, value in updated_data.dict().items():
        setattr(obj, field, value)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_object(db: AsyncSession, obj: BaseModel):
    """Delete object."""
    await db.delete(obj)
    await db.commit()
