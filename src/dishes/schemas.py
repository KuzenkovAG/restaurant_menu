import abc
import uuid
from decimal import Decimal

from pydantic import BaseModel


class DishBaseModel(BaseModel, abc.ABC):
    """Base schema for Dish."""
    title: str
    description: str
    price: str


class Dish(DishBaseModel):
    """Dish model schema."""
    id: uuid.UUID
    price: Decimal


class CreateDish(DishBaseModel):
    """Input schema for creation Dish."""
    pass
