import uuid
from typing import Union

from fastapi import Depends

from src.core.cashe import Cache
from src.menus.repositories import MenuRepository
from src.menus.schemas import Menu, MenuCreateInput, MenuCreateOutput


class MenuService:
    """Service for Menu."""
    def __init__(
                self,
                repository: MenuRepository = Depends(),
                cache: Cache = Depends(),
            ):
        self.repository = repository
        self.cache = cache

    async def get(self, **filters: Union[uuid.UUID, str]) -> Menu:
        """Get menu with filters."""
        key = f"menu_{filters.get('id')}"
        menu_cache = await self.cache.get(key)
        if menu_cache:
            return Menu.model_validate(menu_cache)
        menu = await self.repository.get_object_or_404(**filters)
        await self.cache.set(key, menu)
        return menu

    async def get_all(self) -> list[Menu]:
        """Get all menus."""
        key = "menus"
        menus_cache = await self.cache.get(key=key)
        if menus_cache:
            return [Menu.model_validate(menu) for menu in menus_cache]
        menus = await self.repository.get_all()
        await self.cache.set(key=key, value=menus)
        return menus

    async def create(self, data: MenuCreateInput) -> MenuCreateOutput:
        """Create menu."""
        menu = await self.repository.create(data=data)
        await self.cache.clear("menus")
        return MenuCreateOutput.model_validate(menu)

    async def update(
                self,
                data: MenuCreateInput,
                menu_id: uuid.UUID,
            ) -> MenuCreateOutput:
        """Update menu."""
        menu = await self.repository.update(id=menu_id, data=data)
        await self.cache.clear("menus", f"menu_{menu_id}")
        return MenuCreateOutput.model_validate(menu)

    async def delete(self, menu_id: uuid.UUID) -> None:
        """Delete menu."""
        await self.repository.delete(id=menu_id)
        await self.cache.clear("menus", "submenus", "dishes", f"menu_{menu_id}")
