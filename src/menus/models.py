import uuid

from sqlalchemy import Column, String, Text, UUID
from sqlalchemy.orm import relationship

from src.database import Base


class Menu(Base):
    """Model for Menus."""
    __tablename__ = 'menus'
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(length=128), unique=True, nullable=False)
    description = Column(Text)

    submenus = relationship(
        'SubMenu',
        back_populates="menu",
        cascade='all, delete',
        lazy='selectin'
    )
