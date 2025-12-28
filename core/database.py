from sqlalchemy.orm import declarative_base,relationship,sessionmaker
from sqlalchemy import (Column, Integer, String, DateTime,func,
                        Table,ForeignKey,create_engine,Float)

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
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


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,autoincrement=True)
    first_name = Column(String(20),nullable=False)
    last_name = Column(String(20),nullable=False)
    age = Column(Integer)
    create_date = Column(DateTime(timezone=True),server_default=func.now())
    update_date = Column(DateTime(timezone=True),server_default=func.now())

    expenses = relationship("Expense",secondary=user_expenses,back_populates="users")



class Expense(Base):
    __tablename__= "expenses"

    id = Column(Integer,primary_key=True,autoincrement=True)
    expense_name = Column(String(30),nullable=False)
    mount = Column(Float,nullable=False)
    create_date = Column(DateTime(timezone=True),server_default=func.now())
    update_date = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User",secondary=user_expenses,back_populates="expenses")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


