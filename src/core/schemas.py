import abc

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel, abc.ABC):
    """Base schema."""
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
