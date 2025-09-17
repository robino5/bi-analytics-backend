from decouple import config
from sqlalchemy import URL, create_engine, text, inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase
import threading
import time

# Primary and Backup DB configurations
PRIMARY = {
    "HOST": config("DB_HOST"),
    "PORT": config("DB_PORT", cast=int),
    "NAME": config("DB_NAME"),
    "USER": config("DB_USERNAME"),
    "PASSWORD": config("DB_PASS"),
}

BACKUP = {
    "HOST": config("DB_BACKUP_HOST"),
    "PORT": config("DB_BACKUP_PORT", cast=int),
    "NAME": config("DB_BACKUP_NAME"),
    "USER": config("DB_BACKUP_USERNAME"),
    "PASSWORD": config("DB_BACKUP_PASS"),
}


def make_url(db):
    """Create SQLAlchemy URL for MSSQL."""
    return URL.create(
        "mssql+pyodbc",
        username=db["USER"],
        password=db["PASSWORD"],
        host=db["HOST"],
        port=db["PORT"],
        database=db["NAME"],
        query={
            "driver": "ODBC Driver 17 for SQL Server",
            "TrustServerCertificate": "yes"
        },
    )


class RuntimeEngine:
    """Manage engine with runtime failover and automatic primary recovery."""

    def __init__(self, check_interval=10):
        self.primary_url = make_url(PRIMARY)
        self.backup_url = make_url(BACKUP)
        self.engine = None
        self.current_db = "Primary"
        self.lock = threading.Lock()
        self.check_interval = check_interval  # seconds for background primary check
        self._connect()
        self._start_background_check()

    def _connect(self):
        """Try primary first, then backup if primary is down."""
        for url, name in [(self.primary_url, "Primary"), (self.backup_url, "Backup")]:
            try:
                engine = create_engine(url, echo=False, pool_pre_ping=True)
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                print(f"✅ Connected to {name} DB")
                self.engine = engine
                self.current_db = name
                return
            except OperationalError:
                print(f"⚠️ {name} DB not reachable. Trying next...")
        raise ConnectionError("❌ Both Primary and Backup DBs are down!")

    def get_engine(self):
        """Return an active engine and try reconnect if DB is down."""
        with self.lock:
            try:
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                return self.engine
            except OperationalError:
                print("⚠️ Current DB down. Reconnecting...")
                self._connect()
                return self.engine

    def _background_check(self):
        """Continuously try to reconnect to primary DB in background."""
        while True:
            time.sleep(self.check_interval)
            with self.lock:
                if self.current_db != "Primary":
                    try:
                        engine = create_engine(self.primary_url, echo=False, pool_pre_ping=True)
                        with engine.connect() as conn:
                            conn.execute(text("SELECT 1"))
                        self.engine = engine
                        self.current_db = "Primary"
                        print("🔄 Primary DB is back online. Switched to Primary!")
                    except OperationalError:
                        pass  # primary still down, ignore

    def _start_background_check(self):
        """Start a thread to check primary DB periodically."""
        thread = threading.Thread(target=self._background_check, daemon=True)
        thread.start()


# Initialize runtime engine
runtime_engine = RuntimeEngine()
engine = runtime_engine.get_engine()


class BaseOrm(DeclarativeBase):
    __table_args__ = {"extend_existing": True}

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            + ",".join(
                f"{key}={vars(self).get(key)!r}" for key in inspect(self.__class__).columns.keys()
            )
            + ")"
        )
