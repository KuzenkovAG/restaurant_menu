import abc
import uuid
from decimal import Decimal

from pydantic import Field, model_validator

from src.config import settings
from src.core.schemas import BaseSchema


class DishBaseModel(BaseSchema, abc.ABC):
    """Base schema for Dish."""
    price: Decimal
    discount: Decimal = Field(exclude=True, default=settings.DEFAULT_DISCOUNT)

    @model_validator(mode='after')
    def check_price(self):
        """Return price for customer with discount."""
        price_with_discount = self.price * (1 - self.discount)
        self.price = Decimal(f'{price_with_discount:.2f}')
        return self


class Dish(DishBaseModel):
    """Dish model schema."""
    id: uuid.UUID | str
    submenu_id: str


class CreateDish(DishBaseModel):
    """Input schema for creation Dish."""
    ...


class CreateDishOutput(DishBaseModel):
    """Output schema for creation Dish."""
    id: uuid.UUID | str
