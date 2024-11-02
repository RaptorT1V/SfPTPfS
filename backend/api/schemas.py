from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SensorData(BaseModel):
    value_id: int
    registered_value: datetime
    parameter1: Optional[float]
    parameter2: Optional[float]
    parameter3: Optional[float]
