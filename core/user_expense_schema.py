from pydantic import BaseModel,ConfigDict
from user_schema import UserCreateSchema
from expense_schema import ExpenseCreateSchema

class CreateExpenseWithUserSchema(BaseModel):
    user: UserCreateSchema
    expense: ExpenseCreateSchema
model_config = ConfigDict(from_attributes=True)