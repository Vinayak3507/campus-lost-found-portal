""""Purpose:
Define data validation models.

**Responsibilities:
Validate incoming data for:
user registration
user login

*Also define response format for:
token response
user response

---> Schemas protect your backend from bad input data."""


# from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.models.enums import BranchEnum
from pydantic import ConfigDict



class UserRegisterRequest(BaseModel):
    
    model_config = ConfigDict(
        str_strip_whitespace=True
    )
    student_name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Full name of the student"
    )

    student_id: str = Field(
        ...,
        min_length=5,
        max_length=30,
        description="College issued student ID"
    )

    college_email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        description="Password must contain uppercase, lowercase, digit and special character"
    )

    confirm_password: str

    branch: BranchEnum

    academic_session: str = Field(
        ...,
        pattern=r"^\d{4}-\d{4}$",
        description="Example: 2024-2028"
    )

    block : str | None = None

    phone: str | None = Field(
        default=None,
        pattern=r"^\d{10}$"
    )

    @field_validator("student_name")
    @classmethod
    def validate_student_name(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("Student name cannot be empty.")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter.")

        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter.")

        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit.")

        special_characters = "!@#$%^&*()-_=+[]{}|\\:;\"'<>,.?/"

        if not any(c in special_characters for c in value):
            raise ValueError("Password must contain at least one special character.")
        return value

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, value: str, info):
        password = info.data.get("password")
        if password != value:
            raise ValueError("Passwords do not match.")
        return value