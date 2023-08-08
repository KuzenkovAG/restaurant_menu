import uuid

from fastapi import APIRouter, Depends, status

from . import schemas
from .services import SubMenuService

router = APIRouter(prefix='/menus/{menu_id}/submenus', tags=['SubMenu'])


@router.get('/', response_model=list[schemas.SubMenu], status_code=status.HTTP_200_OK)
async def get_submenus(
    menu_id: uuid.UUID,
    submenu: SubMenuService = Depends(),
) -> list[schemas.SubMenu]:
    """Get list of SubMenus."""
    return await submenu.get_all(menu_id=menu_id)


@router.get(
    '/{submenu_id}',
    response_model=schemas.SubMenu,
    status_code=status.HTTP_200_OK,
)
async def get_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    submenu: SubMenuService = Depends(),
) -> schemas.SubMenu:
    """Get submenu by id."""
    return await submenu.get(submenu_id=submenu_id, menu_id=menu_id)


@router.post(
    '/',
    response_model=schemas.SubMenuCreationOutput,
    status_code=status.HTTP_201_CREATED,
)
async def create_submenu(
    menu_id: uuid.UUID,
    data: schemas.SubMenuCreationInput,
    submenu: SubMenuService = Depends(),
) -> schemas.SubMenuCreationOutput:
    return await submenu.create(data, menu_id=menu_id)


@router.patch(
    '/{submenu_id}',
    response_model=schemas.SubMenuCreationOutput,
    status_code=status.HTTP_200_OK,
)
async def update_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    data: schemas.SubMenuCreationInput,
    submenu: SubMenuService = Depends(),
) -> schemas.SubMenuCreationOutput:
    """Update SubMenu."""
    return await submenu.update(data=data, submenu_id=submenu_id)


@router.delete('/{submenu_id}', status_code=status.HTTP_200_OK)
async def delete_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    submenu: SubMenuService = Depends(),
) -> None:
    """Delete SubMenu."""
    await submenu.delete(menu_id=menu_id, submenu_id=submenu_id)
