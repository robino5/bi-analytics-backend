from .base import BaseModel

__all__ = ["PortfolioMangement"]


class PortfolioMangement(BaseModel):
    particular: str
    amount: float
