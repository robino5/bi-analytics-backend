from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseOrm

__all__ = ["BranchOrm", "TraderOrm", "ClusterManagerOrm"]


class BranchOrm(BaseOrm):
    __tablename__ = "BI_trd_Branch_Info"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255))
    address: Mapped[str] = mapped_column("address", String(255), nullable=True)


class TraderOrm(BaseOrm):
    __tablename__ = "BI_trd_Dealer_info"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255))
    trader_id: Mapped[str] = mapped_column("trader_id", String(255), primary_key=True)
    trader_name: Mapped[str] = mapped_column("trader_name", String(255))


class ClusterManagerOrm(BaseOrm):
    __tablename__ = "BI_trd_Branch_Region_Info"

    branch_code: Mapped[int] = mapped_column("branch_Code", Integer, primary_key=True)
    branch_name: Mapped[str] = mapped_column("branch_Name", String(255))
    region_id: Mapped[int] = mapped_column("region_Id", Integer, primary_key=True)
    region_name: Mapped[str] = mapped_column("region_Name", String(255))
    manager_name: Mapped[str] = mapped_column("username", String(255), primary_key=True)
