import uuid

from src.core.schemas import BaseSchema
from src.submenus.schemas import SubmenuWithRelations


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


class MenuWithRelations(BaseSchema):
    """Menu schema with relations."""
    id: uuid.UUID | str
    submenus: list[SubmenuWithRelations]
