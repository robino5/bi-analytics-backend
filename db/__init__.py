from decouple import config
from sqlalchemy import URL, create_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase

connection_string = URL.create(
    "mssql+pyodbc",
    username=config("DB_USERNAME"),
    password=config("DB_PASS"),
    host=config("DB_HOST"),
    port=config("DB_PORT", cast=int),
    database=config("DB_NAME"),
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "TrustServerCertificate": "yes",
    },
)

engine = create_engine(url=connection_string, echo=False)


class BaseOrm(DeclarativeBase):
    __table_args__ = {"extend_existing": True}

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__!s}("
            + ",".join(
                str(key) + "=" + f"{vars(self).get(key, None)!r}"
                for key in inspect(self.__class__).columns.keys()  # type: ignore[union-attr]
            )
            + ")"
        )
