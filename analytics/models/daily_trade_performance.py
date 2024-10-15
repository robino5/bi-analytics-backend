from datetime import datetime

from pydantic import field_serializer

from .base import BaseModel

__all__ = ["DailyTurnoverPerformance", "DailyMarginLoanUsage", "SectorExposure"]


class CommonLabelModel(BaseModel):
    label: datetime

    @field_serializer("label")
    def serialize_label(self, dt: datetime, _info):
        return dt.strftime("%d-%b-%Y")


class DailyTurnoverPerformance(CommonLabelModel):
    generated: float | None
    target: float | None


class DailyMarginLoanUsage(CommonLabelModel):
    total_allocated: float
    daily_usage: float


class SectorExposure(BaseModel):
    name: str
    value: float
