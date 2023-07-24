import uuid

from sqlalchemy import Column, func, select, String, Text, UUID
from sqlalchemy.orm import column_property, relationship

from src.database import Base
from src.dishes.models import Dish
from src.submenus.models import SubMenu


class Menu(Base):
    """Model for Menus."""
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(length=128), unique=True, nullable=False)
    description = Column(Text)

    submenus = relationship(
        'SubMenu',
        back_populates="menu",
        cascade='all, delete',
        lazy='selectin'
    )

    submenus_count = column_property(
        select(func.count(SubMenu.id))
        .where(SubMenu.menu_id == id)
        .scalar_subquery(),
    )
    dishes_count = column_property(
        select(func.count(Dish.id))
        .where(SubMenu.menu_id == id)
        .where(Dish.submenu_id == SubMenu.id)
        .scalar_subquery(),
    )
