from datetime import datetime
from typing import Annotated

from fastapi import Body, Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from source_db_api.db import crud, models, schemas
from source_db_api.db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health-check")
def health_check():
    return {"message": "Ok"}


@app.post("/data")
def read_data(body: schemas.ReadDataBody, db: Session = Depends(get_db)):
    data = crud.get_data(
        db,
        start_datetime=body.start_datetime,
        end_datetime=body.end_datetime,
        fields=body.fields,
    )

    return data
