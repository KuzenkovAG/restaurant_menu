import abc
import uuid
from typing import List

from pydantic import BaseModel

from src.dishes.schemas import Dish


class SubMenuBaseModel(BaseModel, abc.ABC):
    """Base schema for Dish."""
    title: str
    description: str


class SubMenu(SubMenuBaseModel):
    """SubMenu schema."""
    id: uuid.UUID
    title: str
    menu_id: uuid.UUID
    description: str
    dishes: List[Dish] = []
    dishes_count: int

    class Config:
        from_attributes = True


class SubMenuCreationInput(SubMenuBaseModel):
    """Input schema for creation SubMenu."""
    pass


class SubMenuCreationOutput(SubMenuBaseModel):
    """Output schema for creation SubMenu."""
    id: uuid.UUID
    menu_id: uuid.UUID
