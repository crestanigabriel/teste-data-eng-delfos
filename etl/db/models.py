# SQLAlchemy models

from sqlalchemy import Column, Numeric, TIMESTAMP, String

from .database import Base


class Signal(Base):
    __tablename__ = "signal"

    id = Column(
        String, primary_key=True, unique=True, index=True
    )  # TODO: check each of these parameters' utility
    name = Column(String)


class Data(Base):
    __tablename__ = "data"

    timestamp = Column(
        TIMESTAMP, primary_key=True, unique=True, index=True
    )  # TODO: check each of these parameters' utility
    signal_id = Column(Numeric)
    value = Column(Numeric)
