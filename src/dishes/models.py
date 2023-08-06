import uuid

from sqlalchemy import UUID, Column, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import relationship

from src.database import Base


class Dish(Base):
    """Model for dishes."""

    __tablename__ = "dishes"
    __mapper_args__ = {"confirm_deleted_rows": False}

    id = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    title = Column(String(length=128))
    description = Column(Text)
    submenu_id = Column(
        UUID(as_uuid=False),
        ForeignKey("submenus.id", ondelete="CASCADE"),
    )
    price = Column(Numeric(precision=10, scale=2))

    submenu = relationship("SubMenu", back_populates="dishes")
