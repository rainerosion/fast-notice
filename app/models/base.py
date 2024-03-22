from datetime import datetime

# import sqlalchemy as sa
from sqlalchemy import BigInteger, Column, DateTime, func
from sqlmodel import SQLModel, Field

from app.core.snowflake import generate_snowflake_id


class BaseField(SQLModel):
    # id: str | None = Field(default_factory=lambda: str(generate_snowflake_id()), primary_key=True, sa_type=BigInteger)
    id: int | None = Field(default_factory=generate_snowflake_id, primary_key=True, sa_type=BigInteger)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None, sa_column=Column(DateTime(), onupdate=func.now()))
