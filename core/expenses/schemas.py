from pydantic import BaseModel, field_validator, Field, field_serializer,ConfigDict
import re
from datetime import datetime
from typing import Optional

class BaseExpenseSchema(BaseModel):
    expense_name : str = Field(...,description="Enter your expenses name")
    mount : float = Field(..., gt=0, description="Must be a positive number")

    @field_validator("expense_name")
    def validate_first_name(cls,value):
        if len(value) >= 30:
            raise ValueError("You must use less than 30 characters")
        if not re.fullmatch(r"^[a-zA-Z1-9_ ]+$",value):
            raise ValueError("Title can contain only letters,numbers,(_)")
        return value
    
    @field_serializer("expense_name")
    def serialize_name(self,value):
        return value.title()
    
class ExpenseCreateSchema(BaseExpenseSchema):
    pass

class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None

    model_config = ConfigDict(from_attributes=True)

class ExpenseResponseSchema(BaseExpenseSchema):
    id : int = Field(...,description="Unique identifier of the object")
    create_date : datetime = Field(...,description="Create date and time of the object")
    update_date : datetime = Field(...,description="Update date and time of the object")

    model_config = ConfigDict(from_attributes=True)
class ExpenseUpdateSchema(BaseExpenseSchema):
    pass