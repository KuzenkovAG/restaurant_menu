import abc
import uuid

from pydantic import BaseModel, ConfigDict


class SubMenuBaseModel(BaseModel, abc.ABC):
    """Base schema for Dish."""
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str


class SubMenu(SubMenuBaseModel):
    """SubMenu schema."""
    id: uuid.UUID
    title: str
    menu_id: uuid.UUID
    description: str
    dishes_count: int


class SubMenuCreationInput(SubMenuBaseModel):
    """Input schema for creation SubMenu."""
    pass


class SubMenuCreationOutput(SubMenuBaseModel):
    """Output schema for creation SubMenu."""
    id: uuid.UUID
    menu_id: uuid.UUID
