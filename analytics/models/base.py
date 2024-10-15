from pydantic import BaseModel as Base
from pydantic import ConfigDict


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)
