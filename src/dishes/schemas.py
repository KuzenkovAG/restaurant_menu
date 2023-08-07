import abc
import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DishBaseModel(BaseModel, abc.ABC):
    """Base schema for Dish."""
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    price: Decimal


class Dish(DishBaseModel):
    """Dish model schema."""
    id: uuid.UUID | str
    price: Decimal
    submenu_id: uuid.UUID | str


class CreateDish(DishBaseModel):
    """Input schema for creation Dish."""
    price: Decimal


class CreateDishOutput(DishBaseModel):
    """Output schema for creation Dish."""
    id: uuid.UUID | str
