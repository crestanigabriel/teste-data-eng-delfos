import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Reading variables from .env
load_dotenv()
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_DATABASE_NAME = os.getenv("POSTGRES_DB")
print("----------------------")
print(DB_USER)
print(DB_PASSWORD)
print(DB_HOST)
print(DB_DATABASE_NAME)
print("----------------------")

# Database connection string
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@source_db:5432/{DB_DATABASE_NAME}"
)
print(SQLALCHEMY_DATABASE_URL)
# TODO: remove next line
# print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
