from sqlalchemy import Column, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept as Base


async def get_object(
            db: AsyncSession,
            model: Base,
            many: bool = False,
            **filters: Column[str],
        ):
    """Get object with filters."""
    query = select(model).filter_by(**filters)
    obj = await db.execute(query)
    if many:
        return obj.scalars().all()
    return obj.scalars().first()


async def create_object(db: AsyncSession, data: dict, model: Base):
    """Create object."""
    created_object = model(**data)
    db.add(created_object)
    await db.commit()
    return created_object


async def bulk_create(db: AsyncSession, datas: list[dict], model: Base):
    """Bulk create objects."""
    created_objects = [model(**data) for data in datas]
    db.add_all(created_objects)
    await db.commit()
    return created_objects


async def count_objects(db: AsyncSession, model: Base):
    """Count of model objects."""
    query = select(func.count()).select_from(model)
    objects = await db.execute(query)
    return objects.scalars().first()
