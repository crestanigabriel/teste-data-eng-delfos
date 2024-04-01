from pandas import DataFrame
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def get_signal(db: Session) -> list[models.Signal]:
    query = select(models.Signal)
    result = db.scalars(query).all()

    return result


def create_data(db: Session, data: schemas.DataCreate):
    db_data = models.Data(name="")
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


# def create_signal(db: Session, signal: schemas.SignalCreate):
#     db_signal = models.Signal(name="")
#     db.add(db_signal)
#     db.commit()
#     db.refresh(db_signal)
#     return db_signal


# def create_data(db: Session, data: schemas.DataCreate):
#     db_data = models.Data(timestamp, signal_id, value)
#     db.add(db_data)
#     db.commit()
#     db.refresh(db_data)
#     return db_data
