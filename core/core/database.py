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


user_expenses = Table(
    "users_expenses",
    Base.metadata,
    Column("user_id",Integer,ForeignKey("users.id",ondelete="CASCADE")),
    Column("expense_id",Integer,ForeignKey("expenses.id",ondelete="CASCADE"))
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
