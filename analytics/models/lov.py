from .base import BaseModel

__all__ = ["Branch", "Trader", "ClusterManager"]


class Branch(BaseModel):
    branch_code: int
    branch_name: str
    address: str | None = None


class Trader(BaseModel):
    branch_code: int
    branch_name: str
    trader_id: str
    trader_name: str


class ClusterManager(BaseModel):
    branch_code: int
    branch_name: str
    region_name: str
    region_id: int
    manager_name: str
