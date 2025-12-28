from pydantic import BaseModel, field_validator, Field, field_serializer
import re


class BaseUserSchema(BaseModel):

    first_name : str = Field(...,description="Enter your first name")
    last_name : str = Field(...,description="Enter your last name")
    age : int = Field(..., gt=0, description="Must be a positive number")
    
    @field_validator("first_name")
    def validate_first_name(cls,value):
        if len(value) >= 30:
            raise ValueError("You must use less than 30 characters")
        if not re.fullmatch(r"^[a-zA-Z]+$",value):
            raise ValueError("Title can contain only letters")
        return value

    @field_serializer("first_name")
    def serialize_name(self,value):
        return value.title()
    
    @field_validator("last_name")
    def validate_last_name(cls,value):
        if len(value) >= 30:
            raise ValueError("You must use less than 30 characters")
        if not re.fullmatch(r"^[a-zA-Z]+$",value):
            raise ValueError("Title can contain only letters")
        return value
            
    @field_serializer("last_name")
    def serialize_name(self,value):
        return value.title()

class UserCreateSchema(BaseUserSchema):
    pass


class UserResponseSchema(BaseUserSchema):

    id : int 

class UserUpdateSchema(BaseUserSchema):
    pass
