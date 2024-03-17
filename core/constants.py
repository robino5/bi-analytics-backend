from enum import StrEnum

SECONDS = 60
MINUTE = 30

DEFAULT_CACHE_TIME = SECONDS * MINUTE


class StatusEnum(StrEnum):
    SUCCESS = "success"
    ERROR = "error"
