from pydantic import BaseModel, field_validator, Field, field_serializer
import re


class BaseExpenseSchema(BaseModel):
    expense_name : str = Field(...,description="Enter your expenses name")
    mount : float = Field(..., gt=0, description="Must be a positive number")

    @field_validator("expense_name")
    def validate_first_name(cls,value):
        if len(value) >= 30:
            raise ValueError("You must use less than 30 characters")
        if not re.fullmatch(r"^[a-zA-Z1-9_]+$",value):
            raise ValueError("Title can contain only letters,numbers,(_)")
        return value
    
    @field_serializer("expense_name")
    def serialize_name(self,value):
        return value.title()
    
class ExpenseCreateSchema(BaseExpenseSchema):
    pass


class ExpenseResponseSchema(BaseExpenseSchema):

    id : int 

class ExpenseUpdateSchema(BaseExpenseSchema):
    pass