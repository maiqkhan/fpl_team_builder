from sqlmodel import Field, SQLModel
from datetime import datetime
from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    field_validator,
    ValidationInfo,
    AfterValidator,
)

from typing import Optional, Annotated


class GameweekDeadline(SQLModel, table=True):
    """Gameweek deadline model.
    This model represents the deadline for a specific gameweek in the analytics schema.
    """

    __tablename__ = "GW_DEADLINE"
    __table_args__ = {"schema": "analytics"}

    gameweek: int = Field(
        primary_key=True,
    )
    deadline: datetime = Field(
        sa_column_kwargs={"nullable": False},
    )
