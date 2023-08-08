import uuid

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

    async def get(self, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> schemas.SubMenu:
        """Get submenu by filter."""
        key = f'menu_{menu_id}_submenu_{submenu_id}'
        submenu_cache = await self.cache.get(key)
        if submenu_cache:
            return schemas.SubMenu.model_validate(submenu_cache)
        submenu = await self.repository.get_object_or_404(
            id=submenu_id,
            menu_id=menu_id,
        )
        await self.cache.set(key, submenu)
        return submenu

    async def get_all(self, menu_id: uuid.UUID) -> list[schemas.SubMenu]:
        """Get all submenus."""
        key = f'menu_{menu_id}_submenus'
        submenus_cache = await self.cache.get(key=key)
        if submenus_cache:
            return [schemas.SubMenu.model_validate(submenu) for submenu in submenus_cache]
        submenus = await self.repository.get_all(menu_id=menu_id)
        await self.cache.set(key=key, value=submenus)
        return submenus

    async def create(
        self,
        data: schemas.SubMenuCreationInput,
        menu_id: uuid.UUID,
    ) -> schemas.SubMenuCreationOutput:
        """Create submenu."""
        submenu = await self.repository.create(data=data, menu_id=menu_id)
        await self._clear_cache_of_parents(menu_id=menu_id)
        return schemas.SubMenuCreationOutput.model_validate(submenu)

    async def update(
        self,
        data: schemas.SubMenuCreationInput,
        submenu_id: uuid.UUID,
    ) -> schemas.SubMenuCreationOutput:
        """Update submenu."""
        submenu = await self.repository.update(data=data, id=submenu_id)
        await self.cache.clear(
            f'menu_{submenu.menu_id}_submenus',
            f'menu_{submenu.menu_id}_submenu_{submenu.id}',
        )
        return schemas.SubMenuCreationOutput.model_validate(submenu)

    async def delete(self, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> None:
        """Delete submenu."""
        await self.repository.delete(id=submenu_id)
        await self._clear_cache_of_parents(menu_id=menu_id)
        await self.cache.clear_by_mask(f'menu_{menu_id}_submenu_{submenu_id}')

    async def _clear_cache_of_parents(self, menu_id: uuid.UUID) -> None:
        await self.cache.clear(
            'menus',
            f'menu_{menu_id}',
            f'menu_{menu_id}_submenus',
        )
