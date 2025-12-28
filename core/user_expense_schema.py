from pydantic import BaseModel
from user_schema import UserCreateSchema
from expense_schema import ExpenseCreateSchema

class CreateExpenseWithUserSchema(BaseModel):
    user: UserCreateSchema
    expense: ExpenseCreateSchema

    class Config:
        from_attributes = True