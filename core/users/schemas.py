from pydantic import BaseModel, field_validator, Field, field_serializer, ConfigDict
import re


class UserLoginSchema(BaseModel):
    username: str = Field(..., description="username for user login")
    password: str = Field(..., description="password for user login")


class UserRegisterSchema(BaseModel):
    first_name: str = Field(..., description="Enter your first name")
    last_name: str = Field(None, description="Enter your last name")
    username: str = Field(..., description="username for user login")
    password: str = Field(
        ..., max_length=64, min_length=8, description="password for user login"
    )

    @field_validator("first_name")
    def validate_first_name(cls, value):
        if len(value) >= 21:
            raise ValueError("You must use less than 21 characters")
        if not re.fullmatch(r"^[a-zA-Z]+$", value):
            raise ValueError("Title can contain only letters")
        return value

    @field_serializer("first_name")
    def serialize_name(self, value):
        return value.title()

    @field_validator("last_name")
    def validate_last_name(cls, value):
        if len(value) >= 21:
            raise ValueError("You must use less than 21 characters")
        if not re.fullmatch(r"^[a-zA-Z ]+$", value):
            raise ValueError("Title can contain only letters")
        return value


class UserResponseSchema(BaseModel):
    id: int = Field(..., description="Unique identifier of the object")
    first_name: str = Field(..., description="First name of the user")
    last_name: str | None = Field(None, description="Last name of the user")
    username: str = Field(..., description="Username of the user")

    model_config = ConfigDict(from_attributes=True)


class UserUpdateResponseSchema(BaseModel):
    detail: str
    user: UserResponseSchema

    model_config = ConfigDict(from_attributes=True)
