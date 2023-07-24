import uuid

from sqlalchemy import Column, ForeignKey, Numeric, String, Text, UUID
from sqlalchemy.orm import relationship

from src.database import Base


class Dish(Base):
    """Model for dishes."""
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(length=128))
    description = Column(Text)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))
    price = Column(Numeric(precision=10, scale=2))

    submenu = relationship('SubMenu', back_populates='dishes')
