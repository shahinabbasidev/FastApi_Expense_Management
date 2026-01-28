from pydantic import BaseModel,ConfigDict
from users.schemas import UserRegisterSchema
from expenses.schemas import ExpenseCreateSchema

class CreateExpenseWithUserSchema(BaseModel):
    user: UserRegisterSchema
    expense: ExpenseCreateSchema
model_config = ConfigDict(from_attributes=True)