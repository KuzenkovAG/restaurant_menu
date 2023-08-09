import uuid

from sqlalchemy import UUID, Column, Text

from src.database import Base


class BaseUUIDDescriptionModel(Base):
    """Base model."""
    __abstract__ = True
    id = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    description = Column(Text)
