import uuid

from fastapi import APIRouter, Depends, status

from . import schemas
from .services import MenuService

router = APIRouter(prefix='/menus', tags=['Menu'])


@router.get('/', response_model=list[schemas.Menu], status_code=status.HTTP_200_OK)
async def get_menus(menu: MenuService = Depends()) -> list[schemas.Menu]:
    """Get list of menus."""
    return await menu.get_all()


@router.get(
    '/{menu_id}',
    response_model=schemas.Menu,
    status_code=status.HTTP_200_OK,
)
async def get_menu(menu_id: uuid.UUID, menu: MenuService = Depends()) -> schemas.Menu:
    """Get meny by id."""
    return await menu.get(id=menu_id)


@router.post(
    '/',
    response_model=schemas.MenuCreateOutput,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
    data: schemas.MenuCreateInput,
    menu: MenuService = Depends(),
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
    menu: MenuService = Depends(),
) -> schemas.MenuCreateOutput:
    """Update menu."""
    return await menu.update(data=data, menu_id=menu_id)


@router.delete('/{menu_id}', status_code=status.HTTP_200_OK)
async def delete_menu(menu_id: uuid.UUID, menu: MenuService = Depends()) -> None:
    """Delete menu."""
    await menu.delete(menu_id=menu_id)
