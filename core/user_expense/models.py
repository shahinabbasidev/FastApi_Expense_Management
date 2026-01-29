from sqlalchemy import Table, Column, Integer, ForeignKey
from core.database import Base

user_expenses = Table(
    "users_expenses",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("expense_id", Integer, ForeignKey("expenses.id", ondelete="CASCADE"))
)