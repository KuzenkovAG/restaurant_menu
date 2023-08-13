import uuid

from src.core.schemas import BaseSchema
from src.dishes.schemas import CreateDishOutput


class SubMenu(BaseSchema):
    """SubMenu schema."""
    id: uuid.UUID | str
    menu_id: uuid.UUID
    dishes_count: int


class SubMenuCreationInput(BaseSchema):
    """Input schema for creation SubMenu."""
    ...


class SubMenuCreationOutput(BaseSchema):
    """Output schema for creation SubMenu."""
    id: uuid.UUID | str
    menu_id: uuid.UUID | str


class SubmenuWithRelations(BaseSchema):
    """Submenu with relations."""
    id: uuid.UUID | str
    dishes: list[CreateDishOutput]
