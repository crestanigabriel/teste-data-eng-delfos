# SQLAlchemy models

from sqlalchemy import Column, ForeignKey, Integer, Numeric, TIMESTAMP, String

from .database import Base


class Signal(Base):
    __tablename__ = "signal"

    id = Column(Integer, primary_key=True)
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

    timestamp = Column(TIMESTAMP, primary_key=True)
    signal_id = Column(Integer, ForeignKey("signal.id"), primary_key=True)
    value = Column(Numeric)
