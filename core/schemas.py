from pydantic import BaseModel, field_validator, Field, field_serializer
import re


class BasePersonSchema(BaseModel):

    first_name : str = Field(...,description="Enter your first name")
    last_name : str = Field(...,description="Enter your last name")
    age : int = Field(..., gt=0, description="Must be a positive number")
    expense_name : str = Field(...,description="Enter your expenses name")
    mount : float = Field(..., gt=0, description="Must be a positive number")

    @field_validator("first_name")
    def validate_first_name(cls,value):
        if len(value) >= 30:
            raise ValueError("You must use less than 30 characters")
        if not re.fullmatch(r"^[a-zA-Z]+$",value):
            raise ValueError("Title can contain only letters, numbers, and underscore (_)")
        return value

    @field_serializer("first_name")
    def serialize_name(self,value):
        return value.title()
    
    @field_validator("last_name")
    def validate_last_name(cls,value):
        if len(value) >= 30:
            raise ValueError("You must use less than 30 characters")
        if not re.fullmatch(r"^[a-zA-Z]+$",value):
            raise ValueError("Title can contain only letters, numbers, and underscore (_)")
        return value
            
    @field_serializer("last_name")
    def serialize_name(self,value):
        return value.title()
    
    @field_validator("expense_name")
    def validate_expense_name(cls,value):
        if len(value) >= 40:
            raise ValueError("You must use less than 30 characters")
        if not re.fullmatch(r"^[a-zA-Z0-9_]+$",value):
            raise ValueError("Title can contain only letters, numbers, and underscore (_)")
        return value
    
    @field_serializer("expense_name")
    def serialize_name(self,value):
        return value.title()

class PersonCreateSchema(BasePersonSchema):
    pass


class PersonResponseSchema(BasePersonSchema):

    id : int 

class PersonUpdateSchema(BasePersonSchema):
    pass
