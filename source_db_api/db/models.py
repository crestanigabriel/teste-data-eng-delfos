# SQLAlchemy models

from sqlalchemy import Column, Numeric, TIMESTAMP

from .database import Base


class Data(Base):
    __tablename__ = "data"

    timestamp = Column(TIMESTAMP, primary_key=True)
    wind_speed = Column(Numeric)
    power = Column(Numeric)
    ambient_temperature = Column(Numeric)
