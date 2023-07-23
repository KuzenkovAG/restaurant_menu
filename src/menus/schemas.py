import abc
import uuid
from typing import List

from pydantic import BaseModel

from src.submenus.schemas import SubMenu


class MenuBaseModel(BaseModel, abc.ABC):
    """Base schema for Dish."""
    title: str
    description: str


class Menu(MenuBaseModel):
    """Menu schema."""
    id: uuid.UUID
    submenus: List[SubMenu] = []
    submenus_count: int
    dishes_count: int

    class Config:
        from_attributes = True


class MenuCreateInput(MenuBaseModel):
    """Input schema for creation Menu."""
    pass


class MenuCreateOutput(MenuBaseModel):
    """Output schema for creation Menu."""
    id: uuid.UUID
