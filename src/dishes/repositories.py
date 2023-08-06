import uuid
from typing import Union

from fastapi import Depends
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories import BaseRepository
from src.database import get_async_session
from src.dishes import models
from src.dishes.schemas import CreateDish, Dish


class DishRepository(BaseRepository[models.Dish, Dish, CreateDish]):
    """Working with db for model Dish."""
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        super().__init__(get_schema=Dish, model=models.Dish, session=session)

    async def get_query(self, **filters: Union[uuid.UUID, str]) -> Select:
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
