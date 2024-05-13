from datetime import datetime

from pydantic import BaseModel as Base
from pydantic import ConfigDict, field_serializer

__all__ = ["DailyTurnoverPerformance", "DailyMarginLoanUsage", "SectorExposure"]


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class DailyTurnoverPerformance(BaseModel):
    label: datetime
    generated: float | None
    target: float | None

    @field_serializer("label")
    def serialize_label(self, dt: datetime, _info):
        return dt.strftime("%d-%b-%Y")


class DailyMarginLoanUsage(BaseModel):
    label: datetime
    total_allocated: float
    daily_usage: float

    @field_serializer("label")
    def serialize_label(self, dt: datetime, _info):
        return dt.strftime("%d-%b-%Y")


class SectorExposure(BaseModel):
    name: str
    value: float
