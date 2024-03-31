import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Reading variables from .env
is_inside_docker = os.environ.get("IS_INSIDE_DOCKER", False)
# print(os.environ.get("PYTHONDONTWRITEBYTECODE", False))
# print(os.environ.get("PYTHONUNBUFFERED", False))
# print(os.environ.get("IS_INSIDE_DOCKER", False))
if is_inside_docker:
    print("RUNNING INSIDE DOCKER")
else:
    print("RUNNING OUTSIDE DOCKER")
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv("../../.env"))
    load_dotenv(find_dotenv("../../source_db/.env"))

SOURCE_DB_USER = os.getenv("POSTGRES_USER")
SOURCE_DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
SOURCE_DB_DATABASE_NAME = os.getenv("POSTGRES_DB")

SOURCE_DB_HOST_PORT = os.getenv("SOURCE_DB_HOST_PORT")
if is_inside_docker:
    SOURCE_DB_HOST_NAME = os.getenv("SOURCE_DB_HOST_NAME")
else:
    SOURCE_DB_HOST_NAME = "localhost"
# print("----------------------")
# print(SOURCE_DB_USER)
# print(SOURCE_DB_PASSWORD)
# print(SOURCE_DB_DATABASE_NAME)
# print(SOURCE_DB_HOST_PORT)
# print(SOURCE_DB_HOST_NAME)
# print("----------------------")

# Database connection string
SQLALCHEMY_DATABASE_URL = f"postgresql://{SOURCE_DB_USER}:{SOURCE_DB_PASSWORD}@{SOURCE_DB_HOST_NAME}:{SOURCE_DB_HOST_PORT}/{SOURCE_DB_DATABASE_NAME}"
# TODO: remove next line
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
