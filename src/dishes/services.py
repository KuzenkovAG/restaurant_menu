import uuid
from typing import Annotated

from fastapi import BackgroundTasks, Depends

from src.core.cashe import Cache, get_cache
from src.dishes import schemas
from src.dishes.repositories import DishRepository, get_dish_repository


class DishService:
    def __init__(
        self,
        repository: DishRepository,
        cache: Cache,
        background_tasks: BackgroundTasks = BackgroundTasks(),
    ):
        self.background_tasks = background_tasks
        self.repository = repository
        self.cache = cache

    async def get(self, dish_id: uuid.UUID, submenu_id: uuid.UUID, menu_id: uuid.UUID) -> schemas.Dish:
        """Get dish by filter."""
        key = f'menu_{menu_id}_submenu_{submenu_id}_dish_{dish_id}'
        dish_cache = await self.cache.get(key)
        if dish_cache:
            return schemas.Dish.model_validate(dish_cache)
        dish = await self.repository.get_object_or_404(id=dish_id, submenu_id=submenu_id)
        await self.cache.set(key, schemas.Dish.model_validate(dish))
        return dish

    async def get_all(self, submenu_id: uuid.UUID, menu_id: uuid.UUID) -> list[schemas.Dish]:
        """Get all dishes."""
        key = f'menu_{menu_id}_submenu_{submenu_id}_dishes'
        dishes_cache = await self.cache.get(key=key)
        if dishes_cache:
            return [schemas.Dish.model_validate(dish) for dish in dishes_cache]
        dishes = await self.repository.get_all(submenu_id=submenu_id)
        await self.cache.set(key=key, value=dishes)
        return dishes

    async def create(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        data: schemas.CreateDish,
        **kwargs: uuid.UUID | str,
    ) -> schemas.CreateDishOutput:
        """Create dish."""
        dish = await self.repository.create(data=data, submenu_id=submenu_id, **kwargs)
        self.background_tasks.add_task(self._clear_cache_parents, menu_id=menu_id, submenu_id=submenu_id)
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
        self.background_tasks.add_task(
            self.cache.clear,
            'menus_relations',
            f'menu_{menu_id}_submenu_{submenu_id}_dishes',
            f'menu_{menu_id}_submenu_{submenu_id}_dish_{dish_id}',
        )
        return schemas.CreateDishOutput.model_validate(dish)

    async def delete(self, menu_id: uuid.UUID, submenu_id: uuid.UUID, id: uuid.UUID) -> None:
        """Delete dish."""
        await self.repository.delete(id=id)
        self.background_tasks.add_task(self.cache.clear, f'menu_{menu_id}_submenu_{submenu_id}_dish_{id}')
        self.background_tasks.add_task(self._clear_cache_parents, menu_id=menu_id, submenu_id=submenu_id)

    async def _clear_cache_parents(self, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> None:
        """Clear cache of parents."""
        await self.cache.clear(
            'menus',
            'menus_relations',
            f'menu_{menu_id}',
            f'menu_{menu_id}_submenus',
            f'menu_{menu_id}_submenu_{submenu_id}',
            f'menu_{menu_id}_submenu_{submenu_id}_dishes',
        )


async def get_dish_service(
    background_tasks: BackgroundTasks,
    repository: Annotated[DishRepository, Depends(get_dish_repository)],
    cache: Annotated[Cache, Depends(get_cache)],
) -> DishService:
    return DishService(repository=repository, cache=cache, background_tasks=background_tasks)
