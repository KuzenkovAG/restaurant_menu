import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from . import crud, schemas

router = APIRouter(
    prefix='/menus',
    tags=['Menu']
)


@router.get(
    '/',
    response_model=List[schemas.Menu],
    status_code=status.HTTP_200_OK
)
async def get_menus(db: AsyncSession = Depends(get_async_session)):
    """Get list of menus."""
    menus = await crud.get_menus(db=db)
    return menus


@router.get(
    '/{menu_id}',
    response_model=schemas.Menu,
    status_code=status.HTTP_200_OK
)
async def get_menu(
            menu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session)
        ):
    """Get meny by id."""
    menu = await crud.get_menu(db=db, uid=menu_id)
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found",
        )
    return menu


@router.post(
    '/',
    response_model=schemas.MenuCreateOutput,
    status_code=status.HTTP_201_CREATED
)
async def create_menu(
            menu: schemas.MenuCreateInput,
            db: AsyncSession = Depends(get_async_session)
        ):
    """Create menu."""
    menu_obj = await crud.get_menu_by_tutle(db=db, title=menu.title)
    if menu_obj:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Menu already exist",
        )
    created_menu = await crud.create_menu(db=db, data=menu)
    return created_menu


@router.patch(
    '/{menu_id}',
    response_model=schemas.Menu,
    status_code=status.HTTP_200_OK
)
async def update_menu(
            data: schemas.MenuCreateInput,
            menu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session)
        ):
    """Update menu."""
    menu = await crud.get_menu(db=db, uid=menu_id)
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found",
        )
    menu_new = await crud.update_menu(db=db, menu=menu, updated_data=data)
    return menu_new


@router.delete(
    '/{menu_id}',
    status_code=status.HTTP_200_OK
)
async def delete_menu(
            menu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session)
        ):
    """Delete menu."""
    menu = await crud.get_menu(db=db, uid=menu_id)
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found",
        )
    await crud.delete_menu(db=db, menu=menu)
    return None
