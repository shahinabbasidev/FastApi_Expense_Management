from sqlalchemy import Column, Integer, String, DateTime,func,Float
from sqlalchemy.orm import relationship
from core.database import Base
import user_expense


class ExpenseModel(Base):
    __tablename__= "expenses"

    id = Column(Integer,primary_key=True,autoincrement=True)
    expense_name = Column(String(30),nullable=False)
    mount = Column(Float,nullable=False)
    create_date = Column(DateTime(timezone=True),server_default=func.now())
    update_date = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("UserModel",secondary=user_expense,back_populates="expenses")