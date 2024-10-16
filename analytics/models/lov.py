from .base import BranchInfoBaseModel

__all__ = ["Branch", "Trader", "ClusterManager"]


class Branch(BranchInfoBaseModel):
    address: str | None = None


class Trader(BranchInfoBaseModel):
    trader_id: str
    trader_name: str


class ClusterManager(BranchInfoBaseModel):
    region_name: str
    region_id: int
    manager_name: str
