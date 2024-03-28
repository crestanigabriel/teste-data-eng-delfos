from datetime import datetime
from sqlalchemy.orm import Session

from . import models, schemas


def get_data(db: Session):
    return db.query(models.Data).offset(0).limit(100).all()
