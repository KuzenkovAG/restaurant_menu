import uuid

from src.core.schemas import BaseSchema


class Menu(BaseSchema):
    """Menu schema."""
    id: uuid.UUID | str
    submenus_count: int
    dishes_count: int


class MenuCreateInput(BaseSchema):
    """Input schema for creation Menu."""
    ...


class MenuCreateOutput(BaseSchema):
    """Output schema for creation Menu."""
    id: uuid.UUID | str
