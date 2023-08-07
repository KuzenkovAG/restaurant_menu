import uuid

from sqlalchemy import UUID, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from src.database import Base


class SubMenu(Base):
    """Model for SubMenus."""
    __tablename__ = 'submenus'
    __mapper_args__ = {'confirm_deleted_rows': False}

    id = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    title = Column(String(length=128), unique=True, nullable=False)
    description = Column(Text)
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
