from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from src.core.models import BaseUUIDDescriptionModel


class SubMenu(BaseUUIDDescriptionModel):
    """Model for SubMenus."""
    __tablename__ = 'submenus'
    __mapper_args__ = {'confirm_deleted_rows': False}

    title = Column(String(length=128), unique=True, nullable=False)
    menu_id = Column(
        UUID(as_uuid=False),
        ForeignKey('menus.id', ondelete='CASCADE'),
    )

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship(
        'Dish',
        back_populates='submenu',
        cascade='all, delete',
        lazy='subquery',
    )
