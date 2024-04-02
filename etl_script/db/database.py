import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

ENV_PATH = "../../target_db/.env"

# Reading variables from .env
is_inside_docker = os.environ.get("IS_INSIDE_DOCKER", False)
logging.debug(f"IS_INSIDE_DOCKER: {os.environ.get("IS_INSIDE_DOCKER", False)}")
if not is_inside_docker:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(ENV_PATH))

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_DATABASE_NAME = os.getenv("POSTGRES_DB")

DB_HOST_PORT = os.getenv("DB_HOST_PORT")
if is_inside_docker:
    DB_HOST_NAME = DB_DATABASE_NAME
else:
    DB_HOST_NAME = "localhost"

logging.debug(f"DB_USER: {DB_USER}")
logging.debug(f"DB_PASSWORD: {DB_PASSWORD}")
logging.debug(f"DB_DATABASE_NAME: {DB_DATABASE_NAME}")
logging.debug(f"DB_HOST_PORT: {DB_HOST_PORT}")
logging.debug(f"DB_HOST_NAME: {DB_HOST_NAME}")

# Database connection string
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_NAME}:{DB_HOST_PORT}/{DB_DATABASE_NAME}"
logging.debug(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()
