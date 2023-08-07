import abc
import uuid

from pydantic import BaseModel, ConfigDict


class MenuBaseModel(BaseModel, abc.ABC):
    """Base schema for Dish."""
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str


class Menu(MenuBaseModel):
    """Menu schema."""
    id: uuid.UUID | str
    submenus_count: int
    dishes_count: int


class MenuCreateInput(MenuBaseModel):
    """Input schema for creation Menu."""
    ...


class MenuCreateOutput(MenuBaseModel):
    """Output schema for creation Menu."""
    id: uuid.UUID | str
