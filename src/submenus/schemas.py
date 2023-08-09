import uuid

from src.core.schemas import BaseSchema


class SubMenu(BaseSchema):
    """SubMenu schema."""
    id: uuid.UUID
    menu_id: uuid.UUID
    dishes_count: int


class SubMenuCreationInput(BaseSchema):
    """Input schema for creation SubMenu."""
    ...


class SubMenuCreationOutput(BaseSchema):
    """Output schema for creation SubMenu."""
    id: uuid.UUID
    menu_id: uuid.UUID
