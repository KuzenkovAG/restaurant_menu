import uuid

from sqlalchemy import Column, ForeignKey, func, select, String, Text, UUID
from sqlalchemy.orm import column_property, relationship

from src.database import Base
from src.dishes.models import Dish


class SubMenu(Base):
    """Model for SubMenus."""
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(length=128), unique=True, nullable=False)
    description = Column(Text)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))

    menu = relationship('Menu', back_populates="submenus")
    dishes = relationship(
        "Dish",
        back_populates='submenu',
        cascade='all, delete',
        lazy='selectin',
    )
    dishes_count = column_property(
        select(func.count(Dish.id))
        .where(Dish.submenu_id == id)
        .scalar_subquery(),
    )
