import abc
import uuid
from decimal import Decimal

from src.core.schemas import BaseSchema


class DishBaseModel(BaseSchema, abc.ABC):
    """Base schema for Dish."""
    price: Decimal


class Dish(DishBaseModel):
    """Dish model schema."""
    id: uuid.UUID | str
    submenu_id: uuid.UUID | str


class CreateDish(DishBaseModel):
    """Input schema for creation Dish."""
    ...


class CreateDishOutput(DishBaseModel):
    """Output schema for creation Dish."""
    id: uuid.UUID | str
