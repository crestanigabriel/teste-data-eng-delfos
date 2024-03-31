from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import load_only, Session

from . import models, schemas


def get_data(
    db: Session,
    start_datetime: datetime,
    end_datetime: datetime,
    fields: list[schemas.FieldsEnum],
):
    # return db.query(models.Data).limit(5).all()

    columns = [getattr(models.Data, "timestamp")]

    if not fields:
        columns.append(getattr(models.Data, "wind_speed"))
        columns.append(getattr(models.Data, "power"))
        columns.append(getattr(models.Data, "ambient_temperature"))
    else:
        for field in fields:
            columns.append(getattr(models.Data, field))

    query = (
        select(models.Data)
        .options(load_only(*columns))
        .where(models.Data.timestamp.between(start_datetime, end_datetime))
    )
    result = db.scalars(query).all()

    return result

    return (
        db.query(models.Data)
        # .filter(models.Data.timestamp.between(start_datetime, end_datetime))
        .all()
    )
