from .base import BaseModel, TradingDateModel

__all__ = ["DailyTurnoverPerformance", "DailyMarginLoanUsage", "SectorExposure"]


class DailyTurnoverPerformance(TradingDateModel):
    generated: float | None
    target: float | None


class DailyMarginLoanUsage(TradingDateModel):
    total_allocated: float
    daily_usage: float


class SectorExposure(BaseModel):
    name: str
    value: float
