import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy import Select, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories import BaseRepository
from src.database import get_async_session
from src.dishes.models import Dish
from src.submenus import models
from src.submenus.schemas import SubMenu, SubMenuCreationInput


class SubMenuRepository(BaseRepository[
    models.SubMenu,
    SubMenu,
    SubMenuCreationInput,
]):
    """Working with db for model SubMenu."""

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        super().__init__(get_schema=SubMenu, model=models.SubMenu, session=session)

    async def get_query(self, **filters: uuid.UUID | str) -> Select:
        """Query for get menus."""
        return (
            select(
                self.model.id,
                self.model.title,
                self.model.description,
                self.model.menu_id,
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .filter_by(**filters)
            .outerjoin(Dish, self.model.id == Dish.submenu_id)
            .group_by(self.model.id)
        )

    async def create(
        self,
        data: SubMenuCreationInput,
        **kwargs: uuid.UUID | str,
    ) -> models.SubMenu:
        """Create submenu."""
        submenu = await self.get_all(title=data.title)
        if submenu:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f'Submenu with title - {data.title}, already exist',
            )
        return await self.perform_create(data, **kwargs)
