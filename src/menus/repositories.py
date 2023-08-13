import uuid
from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import Select, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories import BaseRepository
from src.database import get_async_session
from src.dishes.models import Dish
from src.menus import models
from src.menus.schemas import Menu, MenuCreateInput
from src.submenus.models import SubMenu


class MenuRepository(BaseRepository[models.Menu, Menu, MenuCreateInput]):
    """Working with db for model Menu."""

    def __init__(self, session: AsyncSession):
        super().__init__(get_schema=Menu, model=models.Menu, session=session)

    async def get_query(self, **filters: uuid.UUID | str) -> Select:
        """Query for get menus."""
        return (
            select(
                self.model.id,
                self.model.title,
                self.model.description,
                func.count(distinct(SubMenu.id)).label('submenus_count'),
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .filter_by(**filters)
            .outerjoin(SubMenu, self.model.id == SubMenu.menu_id)
            .outerjoin(Dish, SubMenu.id == Dish.submenu_id)
            .group_by(self.model.id)
        )

    async def get_with_relations(self) -> Sequence[models.Menu]:
        """Return query of model."""
        query = select(self.model)
        objects = await self.session.execute(query)
        return objects.scalars().all()

    async def create(
        self,
        data: MenuCreateInput,
        **kwargs: uuid.UUID | str,
    ) -> models.Menu:
        """Create menu."""
        menu = await self.get_all(title=data.title)
        if menu:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f'Menu with title - {data.title}, already exist',
            )
        return await self.perform_create(data, **kwargs)


async def get_menu_repository(session: Annotated[AsyncSession, Depends(get_async_session)]) -> MenuRepository:
    return MenuRepository(session=session)
