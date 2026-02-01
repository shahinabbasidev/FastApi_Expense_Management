from sqlalchemy import Column, Integer, String, DateTime,func,Float,ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class ExpenseModel(Base):
    __tablename__= "expenses"

    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    expense_name = Column(String(30),nullable=False)
    mount = Column(Float,nullable=False)
    create_date = Column(DateTime(timezone=True),server_default=func.now())
    update_date = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("UserModel",back_populates="expenses")