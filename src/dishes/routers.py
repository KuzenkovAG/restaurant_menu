import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from . import crud, schemas

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
            submenu_id: uuid.UUID,
            data: schemas.CreateDish,
            db: AsyncSession = Depends(get_async_session)
        ):
    """Create dish."""
    created_dish = await crud.create_dish(
        db=db, data=data, submenu_id=submenu_id
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
    dish_updated = await crud.update_dish(db=db, updated_data=data, dish=dish)
    return dish_updated


@router.delete(
    '/{dish_id}',
    status_code=status.HTTP_200_OK
)
async def delete_dish(
            dish_id: uuid.UUID,
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
    await crud.delete_dish(db=db, dish=dish)
    return None
