import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()

POSTGRES_USER = os.getenv("USER")
POSTGRES_PASSWORD = os.getenv("PASSWORD")
POSTGRES_DB = os.getenv("DATABASE")
POSTGRES_HOST = os.getenv("HOST")
POSTGRES_PORT = os.getenv("PORT")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


def get_auth_data():
    return {"secret_key": SECRET_KEY, "algorithm": ALGORITHM}


engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"options": "-c client_encoding=utf8"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()