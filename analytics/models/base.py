from datetime import datetime

from pydantic import BaseModel as Base
from pydantic import ConfigDict, field_serializer


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class TradingDateModel(BaseModel):
    trading_date: datetime|None

    @field_serializer("trading_date")
    def serialize_trading_date(self, dt: datetime, _info) -> str:
        return dt.strftime("%d-%b-%y")
    
class PushDateModel(BaseModel):
    push_date: datetime | None

    @field_serializer("push_date")
    def serialize_push_date(self, dt: datetime, _info) -> str:
        return dt.strftime("%d-%b-%y:%I:%M:%S %p").upper()

class BranchInfoBaseModel(BaseModel):
    branch_code: int
    branch_name: str
