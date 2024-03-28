from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from db import crud, models
from db.database import SessionLocal, engine

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


@app.get("/data")
def read_data(db: Session = Depends(get_db)):
    data = crud.get_data(db)
    return data
