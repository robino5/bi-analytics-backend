from pydantic import BaseModel as Base
from pydantic import ConfigDict

__all__ = ["PortfolioMangement"]


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class PortfolioMangement(BaseModel):
    particular: str
    amount: float
