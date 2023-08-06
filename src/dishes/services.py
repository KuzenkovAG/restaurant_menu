import uuid
from typing import Union

from fastapi import Depends

from src.core.cashe import Cache
from src.dishes import schemas
from src.dishes.repositories import DishRepository


class DishService:
    def __init__(
                self,
                repository: DishRepository = Depends(),
                cache: Cache = Depends(),
            ):
        self.repository = repository
        self.cache = cache

    async def get(self, **filters: Union[uuid.UUID, str]) -> schemas.Dish:
        """Get dish by filter."""
        key = f"dish_{filters.get('id')}"
        dish_cache = await self.cache.get(key)
        if dish_cache:
            return schemas.Dish.model_validate(dish_cache)
        dish = await self.repository.get_object_or_404(**filters)
        await self.cache.set(key, schemas.Dish.model_validate(dish))
        return dish

    async def get_all(self, **filters: Union[uuid.UUID, str]) -> list[schemas.Dish]:
        """Get all dishes."""
        key = "dishes"
        dishes_cache = await self.cache.get(key=key)
        if dishes_cache:
            return [schemas.Dish.model_validate(dish) for dish in dishes_cache]
        dishes = await self.repository.get_all(**filters)
        await self.cache.set(key=key, value=dishes)
        return dishes

    async def create(
                self,
                menu_id: uuid.UUID,
                submenu_id: uuid.UUID,
                data: schemas.CreateDish,
            ) -> schemas.CreateDishOutput:
        """Create dish."""
        dish = await self.repository.create(data=data, submenu_id=submenu_id)
        await self.cache.clear(
            "menus",
            "submenus",
            "dishes",
            f"menu_{menu_id}",
            f"submenu_{submenu_id}",
        )
        return schemas.CreateDishOutput.model_validate(dish)

    async def update(
                self,
                menu_id: uuid.UUID,
                submenu_id: uuid.UUID,
                dish_id: uuid.UUID,
                data: schemas.CreateDish,
            ) -> schemas.CreateDishOutput:
        """Update dish."""
        dish = await self.repository.update(data=data, id=dish_id)
        await self.cache.clear(
            "menus",
            "submenus",
            "dishes",
            f"menu_{menu_id}",
            f"submenu_{submenu_id}",
            f"dish_{dish_id}",
        )
        return schemas.CreateDishOutput.model_validate(dish)

    async def delete(
                self,
                menu_id: uuid.UUID,
                submenu_id: uuid.UUID,
                dish_id: uuid.UUID,
            ) -> None:
        """Delete dish."""
        await self.repository.delete(id=dish_id)
        await self.cache.clear(
            "menus",
            "submenus",
            "dishes",
            f"menu_{menu_id}",
            f"submenu_{submenu_id}",
            f"dish_{dish_id}",
        )
