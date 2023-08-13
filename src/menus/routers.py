import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.menus import schemas
from src.menus.services import MenuService, get_menu_service

router = APIRouter(prefix='/menus', tags=['Menu'])


@router.get('/', response_model=list[schemas.Menu], status_code=status.HTTP_200_OK)
async def get_menus(menu: Annotated[MenuService, Depends(get_menu_service)]) -> list[schemas.Menu]:
    """Get list of menus."""
    return await menu.get_all()


@router.get(
    '/{menu_id}',
    response_model=schemas.Menu,
    status_code=status.HTTP_200_OK,
)
async def get_menu(menu_id: uuid.UUID, menu: Annotated[MenuService, Depends(get_menu_service)]) -> schemas.Menu:
    """Get meny by id."""
    return await menu.get(id=menu_id)


@router.get(
    '/relations/',
    response_model=list[schemas.MenuWithRelations],
    status_code=status.HTTP_200_OK,
)
async def get_menu_with_relations(
        menu: Annotated[MenuService, Depends(get_menu_service)],
) -> list[schemas.MenuWithRelations]:
    """Get meny with relations."""
    return await menu.get_with_relations()


@router.post(
    '/',
    response_model=schemas.MenuCreateOutput,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
    data: schemas.MenuCreateInput,
    menu: Annotated[MenuService, Depends(get_menu_service)],
) -> schemas.MenuCreateOutput:
    """Create menu."""
    return await menu.create(data=data)


@router.patch(
    '/{menu_id}',
    response_model=schemas.MenuCreateOutput,
    status_code=status.HTTP_200_OK,
)
async def update_menu(
    data: schemas.MenuCreateInput,
    menu_id: uuid.UUID,
    menu: Annotated[MenuService, Depends(get_menu_service)],
) -> schemas.MenuCreateOutput:
    """Update menu."""
    return await menu.update(data=data, menu_id=menu_id)


@router.delete('/{menu_id}', status_code=status.HTTP_200_OK)
async def delete_menu(menu_id: uuid.UUID, menu: Annotated[MenuService, Depends(get_menu_service)]) -> None:
    """Delete menu."""
    await menu.delete(id=menu_id)
