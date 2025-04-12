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


class FormPlayers(SQLModel, table=True):
    """Form players model.
    This model represents the form players in the analytics schema.
    """

    __tablename__ = "FORM_PLAYERS"
    __table_args__ = {"schema": "analytics"}

    player_id: int = Field(primary_key=True, nullable=False)
    full_name: str = Field(nullable=False)
    position: str = Field(nullable=False)
    team: str = Field(nullable=False)
    form: float = Field(nullable=False)
    price: float = Field(nullable=False)
    ownership: float = Field(nullable=False)
    picture_id: int = Field(nullable=False)
