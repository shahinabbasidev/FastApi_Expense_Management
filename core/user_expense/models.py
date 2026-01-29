from sqlalchemy import Table, column, Integer, ForeignKey
from core.database import Base

user_expenses = Table(
    "users_expenses",
    Base.metadata,
    column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    column("expense_id", Integer, ForeignKey("expenses.id", ondelete="CASCADE"))
)