# Pydantic models

from pydantic import BaseModel


class SignalCreate(BaseModel):
    id: int
    name: str
    func: str

    class Config:
        orm_mode = True


class DataCreate(BaseModel):
    timestamp: str
    signal_id: int
    value: float

    class Config:
        orm_mode = True
