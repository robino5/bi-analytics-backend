from datetime import datetime

from pydantic import BaseModel as Base
from pydantic import ConfigDict, field_serializer

__all__ = ["BoardTurnOver", "BoardTurnOverBreakdown"]


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class BoardTurnOver(BaseModel):
    trading_date: datetime
    board: str
    turnover: float
    dse_percentage: float
    lbsl_turnover: float
    lbsl_percentage: float

    @field_serializer("trading_date")
    def serialize_trading_date(self, dt: datetime, _info) -> str:
        return dt.strftime("%d-%b-%Y")


class BoardTurnOverBreakdown(BoardTurnOver):
    pass
