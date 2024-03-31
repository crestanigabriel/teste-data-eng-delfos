# # Pydantic models

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


# class Data(BaseModel):
#     timestamp: datetime
#     wind_speed: float
#     power: float
#     ambient_temperature: float

#     class Config:
#         orm_mode = True


# read_data Request
class FieldsEnum(str, Enum):
    wind_speed = "wind_speed"
    power = "power"
    ambient_temperature = "ambient_temperature"


class ReadDataBody(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    fields: list[FieldsEnum] = None


# read_data Response
# class ReadDataResponse(BaseModel):
#     start_datetime: datetime
#     end_datetime: datetime
