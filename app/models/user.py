from sqlmodel import Field, SQLModel

from app.models.base import BaseField


class User(BaseField, table=True):
    username: str = Field(max_length=50)
    email: str = Field(max_length=100)
    password: str = Field(max_length=100)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class UserCreate(SQLModel):
    username: str
    email: str
    password: str
