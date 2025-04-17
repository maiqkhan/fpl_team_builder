from sqlmodel import Field, SQLModel
from datetime import datetime, date
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


class KeyFixtures(SQLModel, table=True):
    """Key fixtures model.
    This model represents the key fixtures reported in the landing dashboard.
    """

    __tablename__ = "KEY_FIXTURES"
    __table_args__ = {"schema": "analytics"}

    fixture_id: int = Field(primary_key=True, nullable=False)
    home_team: str = Field(nullable=False)
    home_team_picture_id: int = Field(nullable=False)
    away_team: str = Field(nullable=False)
    away_team_picture_id: int = Field(nullable=False)
    ownership_score: float = Field(nullable=False)


class PriceChanges(SQLModel, table=True):
    """Price changes model.
    This model represents the price changes in the analytics schema."""

    __tablename__ = "PRICE_CHANGES"
    __table_args__ = {"schema": "analytics"}

    player_id: int = Field(primary_key=True, nullable=False)
    player_name: str = Field(nullable=False)
    player_position: str = Field(nullable=False)
    player_team: str = Field(nullable=False)
    picture_id: int = Field(nullable=False)
    current_price: float = Field(nullable=False)
    price_up_down: str = Field(nullable=False)
    price_change_date: date = Field(nullable=False)
