from sqlalchemy import UUID, Column, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from src.config import settings
from src.core.models import BaseUUIDDescriptionModel


class Dish(BaseUUIDDescriptionModel):
    """Model for dishes."""

    __tablename__ = 'dishes'
    __mapper_args__ = {'confirm_deleted_rows': False}

    title = Column(String(length=128))
    price = Column(Numeric(precision=10, scale=2))
    submenu_id = Column(
        UUID(as_uuid=False),
        ForeignKey('submenus.id', ondelete='CASCADE'),
    )
    discount = Column(Numeric(precision=5, scale=2), default=settings.DEFAULT_DISCOUNT)

    submenu = relationship('SubMenu', back_populates='dishes')
