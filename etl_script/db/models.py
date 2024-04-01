# SQLAlchemy models

from sqlalchemy import Column, ForeignKey, Integer, Numeric, TIMESTAMP, String

from .database import Base


class Signal(Base):
    __tablename__ = "signal"

    id = Column(
        Integer, primary_key=True, unique=True, index=True
    )  # TODO: check each of these parameters' utility
    name = Column(String)
    func = Column(String)

    # For Pandas DataFrame conversion
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "func": self.func,
        }


class Data(Base):
    __tablename__ = "data"

    timestamp = Column(
        TIMESTAMP, primary_key=True, unique=True, index=True
    )  # TODO: check each of these parameters' utility
    signal_id = Column(Integer, ForeignKey("signal.id"))
    value = Column(Numeric)
