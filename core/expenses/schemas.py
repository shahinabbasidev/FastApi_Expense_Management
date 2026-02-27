from pydantic import (
    BaseModel,
    field_validator,
    Field,
    field_serializer,
    ConfigDict,
)
import re
from datetime import datetime


class BaseExpenseSchema(BaseModel):
    expense_name: str = Field(..., description="Enter your expenses name")
    mount: float = Field(..., gt=0, description="Must be a positive number")
    is_complete: bool = Field(False, description="Whether the expense has been completed")

    @field_validator("expense_name")
    def validate_first_name(cls, value):
        if len(value) >= 30:
            raise ValueError("You must use less than 30 characters")
        # allow digits including zero, letters, underscores and spaces
        if not re.fullmatch(r"^[a-zA-Z0-9_ ]+$", value):
            raise ValueError("Title can contain only letters, numbers, underscore or space")
        return value

    @field_serializer("expense_name")
    def serialize_name(self, value):
        return value.title()


class ExpenseCreateSchema(BaseExpenseSchema):
    pass


class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None

    model_config = ConfigDict(from_attributes=True)


class ExpenseResponseSchema(BaseExpenseSchema):
    id: int = Field(..., description="Unique identifier of the object")
    create_date: datetime = Field(
        ..., description="Create date and time of the object"
    )
    update_date: datetime = Field(
        ..., description="Update date and time of the object"
    )

    model_config = ConfigDict(from_attributes=True)

    model_config = ConfigDict(from_attributes=True)


class ExpenseUpdateSchema(BaseExpenseSchema):
    pass
