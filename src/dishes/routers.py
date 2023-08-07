import uuid

from fastapi import APIRouter, Depends, status

from . import schemas
from .services import DishService

router = APIRouter(
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Dish'],
)


@router.get('/', response_model=list[schemas.Dish], status_code=status.HTTP_200_OK)
async def get_dishes(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dishes: DishService = Depends(),
) -> list[schemas.Dish]:
    """Get list of dishes."""
    return await dishes.get_all(submenu_id=submenu_id)


@router.get('/{dish_id}', response_model=schemas.Dish, status_code=status.HTTP_200_OK)
async def get_dish(
    dish_id: uuid.UUID,
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dishes: DishService = Depends(),
) -> schemas.Dish:
    """Get dish by id."""
    return await dishes.get(id=dish_id, submenu_id=submenu_id)


@router.post('/', response_model=schemas.CreateDishOutput, status_code=status.HTTP_201_CREATED)
async def create_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    data: schemas.CreateDish,
    dishes: DishService = Depends(),
) -> schemas.CreateDishOutput:
    """Create dish."""
    return await dishes.create(menu_id=menu_id, submenu_id=submenu_id, data=data)


@router.patch(
    '/{dish_id}',
    response_model=schemas.CreateDishOutput,
    status_code=status.HTTP_200_OK,
)
async def update_dish(
    data: schemas.CreateDish,
    dish_id: uuid.UUID,
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dishes: DishService = Depends(),
) -> schemas.CreateDishOutput:
    """update dish."""
    return await dishes.update(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        data=data,
    )


@router.delete('/{dish_id}', status_code=status.HTTP_200_OK)
async def delete_dish(
    dish_id: uuid.UUID,
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dishes: DishService = Depends(),
) -> None:
    """Delete dish."""
    await dishes.delete(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
