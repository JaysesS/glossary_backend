from pydantic import BaseModel, validator
from datetime import datetime

def datetime_to_ts(d: datetime) -> int:
    return int(d.timestamp())

class TimeMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: datetime_to_ts
        }
