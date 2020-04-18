from datetime import datetime

from pydantic import BaseModel
from pydantic import conint
from pydantic import validator


class CounterInput(BaseModel):
    increment_by: conint(gt=0)


class CounterResponse(BaseModel):
    incremented_by: int = None
    current_counter: float
    status: str
    timestamp_utc: datetime = None

    @validator("timestamp_utc", pre=True, always=True)
    def set_timestamp(cls, value):
        return datetime.utcnow()


class MetricsCounter(BaseModel):
    produced_records: int
    consumed_records: int
    timestamp_utc: datetime = None

    @validator("timestamp_utc", pre=True, always=True)
    def set_timestamp(cls, value):
        return datetime.utcnow()
