import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import crud as crud_core
from src.database import get_async_session

from . import crud, models, schemas

router = APIRouter(
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Dish']
)


@router.get(
    '/',
    response_model=List[schemas.Dish],
    status_code=status.HTTP_200_OK
)
async def get_dishes(
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session),
        ):
    """Get list of Dishes."""
    submenus = await crud.get_dishes(db=db, submenu_id=submenu_id)
    return submenus


@router.get(
    '/{dish_id}',
    response_model=schemas.Dish,
    status_code=status.HTTP_200_OK
)
async def get_dish(
            dish_id: uuid.UUID,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session)
        ):
    """Get dish by id."""
    menu = await crud.get_dish(
        db=db, dish_uid=dish_id, submenu_uid=submenu_id
    )
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="dish not found",
        )
    return menu


@router.post(
    '/',
    response_model=schemas.Dish,
    status_code=status.HTTP_201_CREATED
)
async def create_dish(
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            data: schemas.CreateDish,
            db: AsyncSession = Depends(get_async_session)
        ):
    """Create dish."""
    data = data.dict()
    data['submenu_id'] = submenu_id
    created_dish = await crud_core.create_object(
        db=db, data=data, model=models.Dish
    )
    return created_dish


@router.patch(
    '/{dish_id}',
    response_model=schemas.Dish,
    status_code=status.HTTP_200_OK
)
async def update_dish(
            data: schemas.CreateDish,
            dish_id: uuid.UUID,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session)
        ):
    """update dish."""
    dish = await crud.get_dish(
        db=db, dish_uid=dish_id, submenu_uid=submenu_id
    )
    if dish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dish not found",
        )
    dish_updated = await crud_core.update_object(
        db=db, updated_data=data, obj=dish
    )
    return dish_updated


@router.delete(
    '/{dish_id}',
    status_code=status.HTTP_200_OK
)
async def delete_dish(
            dish_id: uuid.UUID,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session)
        ):
    dish = await crud.get_dish(
        db=db, dish_uid=dish_id, submenu_uid=submenu_id
    )
    if dish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="dish not found",
        )
    await crud_core.delete_object(db=db, obj=dish)
    return None
