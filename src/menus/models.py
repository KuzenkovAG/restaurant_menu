from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.core.models import BaseUUIDDescriptionModel


class Menu(BaseUUIDDescriptionModel):
    """Model for Menus."""
    __tablename__ = 'menus'
    __mapper_args__ = {'confirm_deleted_rows': False}

    title = Column(String(length=128), unique=True, nullable=False)

    submenus = relationship(
        'SubMenu',
        back_populates='menu',
        cascade='all, delete',
        lazy='selectin',
    )
