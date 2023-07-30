import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import crud as crud_core
from src.database import get_async_session

from . import crud,  models, schemas

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
            data: schemas.MenuCreateInput,
            db: AsyncSession = Depends(get_async_session)
        ):
    """Create menu."""
    existed_menu = await crud_core.get_object_by_title(
        db=db, title=data.title, model=models.Menu
    )
    if existed_menu:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Menu already exist",
        )
    data = data.model_dump()
    menu = await crud_core.create_object(
        db=db, data=data, model=models.Menu
    )
    return menu


@router.patch(
    '/{menu_id}',
    response_model=schemas.MenuCreateOutput,
    status_code=status.HTTP_200_OK
)
async def update_menu(
            data: schemas.MenuCreateInput,
            menu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session)
        ):
    """Update menu."""
    existed_menu = await crud_core.get_object(
        db=db,
        model=models.Menu,
        uid=menu_id
    )
    if existed_menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found",
        )
    menu = await crud_core.update_object(
        db=db, obj=existed_menu, updated_data=data
    )
    return menu


@router.delete(
    '/{menu_id}',
    status_code=status.HTTP_200_OK
)
async def delete_menu(
            menu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session)
        ):
    """Delete menu."""
    menu = await crud_core.get_object(db=db, uid=menu_id, model=models.Menu)
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found",
        )
    await crud_core.delete_object(db=db, obj=menu)
    return None
