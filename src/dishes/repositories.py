import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories import BaseRepository
from src.database import get_async_session
from src.dishes import models
from src.dishes.schemas import CreateDish, Dish


class DishRepository(BaseRepository[models.Dish, Dish, CreateDish]):
    """Working with db for model Dish."""

    def __init__(self, session: AsyncSession):
        super().__init__(get_schema=Dish, model=models.Dish, session=session)

    async def get_query(self, **filters: uuid.UUID | str) -> Select:
        """Query for get dishes."""
        return (
            select(
                self.model.id,
                self.model.title,
                self.model.description,
                self.model.submenu_id,
                self.model.price,
            )
            .filter_by(**filters)
            .group_by(self.model.id)
        )


async def get_dish_repository(session: Annotated[AsyncSession, Depends(get_async_session)]) -> DishRepository:
    return DishRepository(session=session)
