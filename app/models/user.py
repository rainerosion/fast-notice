import re

from pydantic import field_validator
from sqlmodel import Field, SQLModel

from app.models.base import BaseField


class User(BaseField, table=True):
    username: str = Field(max_length=50)
    email: str = Field(max_length=50)
    password: str = Field(max_length=200)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class UserCreate(SQLModel):
    username: str = Field(max_length=50)
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email format")
        return v


class UserUpdate(SQLModel):
    username: str
    email: str
    password: str


class UserOut(SQLModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool
