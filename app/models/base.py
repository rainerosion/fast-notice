from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field

from app.core.snowflake import generate_snowflake_id


class BaseField(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None,
                                        sa_column=Column(DateTime(), onupdate=func.now()))
