import uuid
from typing import Generic, TypeVar, Union

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Select, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base

T_Model = TypeVar("T_Model", bound=Base)
T_Schema = TypeVar("T_Schema", bound=BaseModel)
T_InputSchema = TypeVar("T_InputSchema", bound=BaseModel)


class BaseRepository(Generic[T_Model, T_Schema, T_InputSchema]):
    """Base class for working with db."""
    def __init__(self, get_schema: type[T_Schema], model: type[T_Model], session: AsyncSession):
        self.get_schema = get_schema
        self.model = model
        self.session = session

    async def get_object_or_404(self, **filters: Union[uuid.UUID, str]) -> T_Schema:
        """Return object or 404 if object not exists."""
        obj = await self.get_all(**filters)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__.lower()} not found",
            )
        return obj[0]

    async def get_all(self, **filters: Union[uuid.UUID, str]) -> list[T_Schema]:
        """Get objects by filters."""
        query = await self.get_query(**filters)
        objects = await self.session.execute(query)
        results = objects.all()
        return [self.get_schema.model_validate(result) for result in results]

    async def get_query(self, **filters: Union[uuid.UUID, str]) -> Select:
        """Get query."""
        return select(self.model).filter_by(**filters)

    async def create(self, data: T_InputSchema, **kwargs: Union[uuid.UUID, str]) -> T_Model:
        """Create object."""
        return await self.perform_create(data, **kwargs)

    async def perform_create(self, data: T_InputSchema, **kwargs: Union[uuid.UUID, str]) -> T_Model:
        """Perform create object."""
        obj = self.model(**data.model_dump(), **kwargs)
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def update(self, data: T_InputSchema, **filters: Union[uuid.UUID, str]) -> T_Model:
        """Update object."""
        await self.get_object_or_404(**filters)
        query = (
            update(self.model)
            .values(**data.model_dump())
            .returning(self.model)
            .filter_by(**filters)
        )
        obj = await self.session.execute(query)
        await self.session.commit()
        return obj.scalars().one()

    async def delete(self, **filters: Union[uuid.UUID, str]) -> None:
        """Delete object."""
        await self.get_object_or_404(**filters)
        query = delete(self.model).filter_by(**filters)
        await self.session.execute(query)
        await self.session.commit()
