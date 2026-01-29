from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import (Column, Integer,Table,ForeignKey,create_engine)
from sqlalchemy import create_engine
from core.config import settings

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False
                  }
)


SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
session = SessionLocal()


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
