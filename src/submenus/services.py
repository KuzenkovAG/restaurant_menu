import uuid
from typing import Union

from fastapi import Depends

from src.core.cashe import Cache
from src.submenus import schemas
from src.submenus.repositories import SubMenuRepository


class SubMenuService:
    def __init__(
                self,
                repository: SubMenuRepository = Depends(),
                cache: Cache = Depends(),
            ):
        self.repository = repository
        self.cache = cache

    async def get(self, **filters: Union[uuid.UUID, str]) -> schemas.SubMenu:
        """Get submenu by filter."""
        key = f"submenu_{filters.get('id')}"
        submenu_cache = await self.cache.get(key)
        if submenu_cache:
            return schemas.SubMenu.model_validate(submenu_cache)
        submenu = await self.repository.get_object_or_404(**filters)
        await self.cache.set(key, submenu)
        return submenu

    async def get_all(self, **filters: Union[uuid.UUID, str]) -> list[schemas.SubMenu]:
        """Get all submenus."""
        key = "submenus"
        submenus_cache = await self.cache.get(key=key)
        if submenus_cache:
            return [schemas.SubMenu.model_validate(submenu) for submenu in submenus_cache]
        submenus = await self.repository.get_all(**filters)
        await self.cache.set(key=key, value=submenus)
        return submenus

    async def create(
                self,
                data: schemas.SubMenuCreationInput,
                **filters: Union[uuid.UUID, str],
            ) -> schemas.SubMenuCreationOutput:
        """Create submenu."""
        submenu = await self.repository.create(data=data, **filters)
        await self.cache.clear(
            "menus",
            "submenus",
            f"menu_{submenu.menu_id}",
        )
        return schemas.SubMenuCreationOutput.model_validate(submenu)

    async def update(
                self,
                data: schemas.SubMenuCreationInput,
                submenu_id: uuid.UUID,
            ) -> schemas.SubMenuCreationOutput:
        """Update submenu."""
        submenu = await self.repository.update(data=data, id=submenu_id)
        await self.cache.clear(
            "menus",
            "submenus",
            f"menu_{submenu.menu_id}",
            f"submenu_{submenu.id}",
        )
        return schemas.SubMenuCreationOutput.model_validate(submenu)

    async def delete(self, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> None:
        """Delete submenu."""
        await self.repository.delete(id=submenu_id)
        await self.cache.clear(
            "menus",
            "submenus",
            "dishes",
            f"menu_{menu_id}",
            f"submenu_{submenu_id}",
        )
