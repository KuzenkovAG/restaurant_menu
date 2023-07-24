import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import crud as crude_core
from src.database import get_async_session

from . import crud, models, schemas

router = APIRouter(
    prefix='/menus/{menu_id}/submenus',
    tags=['SubMenu']
)


@router.get(
    '/',
    response_model=List[schemas.SubMenu],
    status_code=status.HTTP_200_OK
)
async def get_submenus(
            menu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session),
        ):
    """Get list of SubMenus."""
    submenus = await crud.get_submenus(db=db, menu_id=menu_id)
    return submenus


@router.get(
    '/{submenu_id}',
    response_model=schemas.SubMenu,
    status_code=status.HTTP_200_OK
)
async def get_submenu(
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session)
        ):
    """Get submenu by id."""
    menu = await crud.get_submenu(
        db=db, menu_uid=menu_id, submenu_uid=submenu_id
    )
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="submenu not found",
        )
    return menu


@router.post(
    '/',
    response_model=schemas.SubMenuCreationOutput,
    status_code=status.HTTP_201_CREATED
)
async def create_submenu(
            menu_id: uuid.UUID,
            data: schemas.SubMenuCreationInput,
            db: AsyncSession = Depends(get_async_session)
        ):
    submenu_obj = await crude_core.get_object_by_title(
        db=db, title=data.title, model=models.SubMenu
    )
    if submenu_obj:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Submenu already exist",
        )
    data = data.dict()
    data['menu_id'] = menu_id
    created_submenu = await crude_core.create_object(
        db=db, data=data, model=models.SubMenu
    )
    return created_submenu


@router.patch(
    '/{submenu_id}',
    response_model=schemas.SubMenu,
    status_code=status.HTTP_200_OK
)
async def update_submenu(
            data: schemas.SubMenuCreationInput,
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session)
        ):
    """Update SubMenu."""
    submenu = await crud.get_submenu(
        db=db, menu_uid=menu_id, submenu_uid=submenu_id
    )
    if submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submenu not found",
        )
    submenu_new = await crude_core.update_object(
        db=db, updated_data=data, obj=submenu,
    )
    return submenu_new


@router.delete('/{submenu_id}', status_code=status.HTTP_200_OK)
async def delete_submenu(
            menu_id: uuid.UUID,
            submenu_id: uuid.UUID,
            db: AsyncSession = Depends(get_async_session)
        ):
    submenu = await crud.get_submenu(
        db=db, menu_uid=menu_id, submenu_uid=submenu_id
    )
    if submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="submenu not found",
        )
    await crude_core.delete_object(db=db, obj=submenu)
    return None
