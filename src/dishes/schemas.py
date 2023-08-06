import abc
import uuid
from decimal import Decimal
from typing import Union

from pydantic import BaseModel, ConfigDict


class DishBaseModel(BaseModel, abc.ABC):
    """Base schema for Dish."""
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    price: Decimal


class Dish(DishBaseModel):
    """Dish model schema."""
    id: Union[uuid.UUID, str]
    price: Decimal
    submenu_id: Union[uuid.UUID, str]


class CreateDish(DishBaseModel):
    """Input schema for creation Dish."""
    price: Decimal


class CreateDishOutput(DishBaseModel):
    """Output schema for creation Dish."""
    id: Union[uuid.UUID, str]
