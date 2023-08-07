from fastapi import APIRouter, FastAPI

from src.dishes.routers import router as dish_router
from src.menus.routers import router as menu_router
from src.submenus.routers import router as submenu_router

app = FastAPI(title='Restaurant menu')

main_router = APIRouter(prefix='/api/v1')
main_router.include_router(menu_router)
main_router.include_router(submenu_router)
main_router.include_router(dish_router)

app.include_router(main_router)
