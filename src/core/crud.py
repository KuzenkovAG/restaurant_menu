import uuid
from typing import Dict, List

from pydantic import BaseModel
from sqlalchemy import func, RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept as Base


async def get_object(db: AsyncSession, model: Base, uid: uuid):
    """Get object by id."""
    query = select(model).filter(model.id == uid)
    obj = await db.execute(query)
    return obj.scalars().first()


async def get_objects(
            db: AsyncSession,
            model: Base
        ):
    """Get objects."""
    query = select(model)
    obj = await db.execute(query)
    return obj.scalars().all()


async def get_object_by_title(
            db: AsyncSession,
            title: str,
            model: Base
        ):
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


async def bulk_create(
            db: AsyncSession,
            datas: List[Dict],
            model: Base
        ):
    """Bulk create objects."""
    created_objects = [model(**data) for data in datas]
    db.add_all(created_objects)
    await db.commit()
    return created_objects


async def update_object(
            db: AsyncSession,
            updated_data: BaseModel,
            obj: RowMapping
        ):
    """Update object."""
    for field, value in updated_data.model_dump().items():
        setattr(obj, field, value)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_object(db: AsyncSession, obj: BaseModel):
    """Delete object."""
    await db.delete(obj)
    await db.commit()


async def count_objects(db: AsyncSession, model: Base):
    """Count of model objects."""
    query = select(func.count()).select_from(model)
    objects = await db.execute(query)
    return objects.scalars().first()
