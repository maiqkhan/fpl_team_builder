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
from typing import Optional


class dim_team(SQLModel, table=True):
    __tablename__ = "dim_team"
    __table_args__ = {"schema": "fpl"}

    team_key: Optional[int] = Field(primary_key=True)
    team_id: int = Field(sa_column_kwargs={"nullable": False})
    full_name: int = Field(sa_column_kwargs={"nullable": False})
    short_name: int = Field(sa_column_kwargs={"nullable": False})
    overall_strength: int = Field(sa_column_kwargs={"nullable": False})
    home_overall_strength: int = Field(sa_column_kwargs={"nullable": False})
    home_attack_strength: int = Field(sa_column_kwargs={"nullable": False})
    home_defence_strength: int = Field(sa_column_kwargs={"nullable": False})
    away_overall_strength: int = Field(sa_column_kwargs={"nullable": False})
    away_attack_strength: int = Field(sa_column_kwargs={"nullable": False})
    away_defence_strength: int = Field(sa_column_kwargs={"nullable": False})
    effective_dt: date = Field(sa_column_kwargs={"nullable": False})
    expiry_dt: date = Field(sa_column_kwargs={"nullable": False})
    current_ind: bool = Field(sa_column_kwargs={"nullable": False})


class dim_fixture(SQLModel, table=True):
    __tablename__ = "dim_fixture"
    __table_args__ = {"schema": "fpl"}

    fixture_key: Optional[int] = Field(primary_key=True)
    fixture_id: int = Field(sa_column_kwargs={"nullable": False})
    season: str = Field(sa_column_kwargs={"nullable": False})
    gameweek: int = Field(sa_column_kwargs={"nullable": False})
    finished_ind: bool = Field(sa_column_kwargs={"nullable": False})
    home_team_key: int = Field(
        foreign_key="dim_team.team_key",
        sa_column_kwargs={"nullable": False},
    )
    away_team_key: int = Field(
        foreign_key="dim_team.team_key",
        sa_column_kwargs={"nullable": False},
    )
    kickoff_time: datetime = Field(sa_column_kwargs={"nullable": False})

    fixture_type: str = Field(sa_column_kwargs={"nullable": False})


class dim_player(SQLModel, table=True):
    __tablename__ = "dim_player"
    __table_args__ = {"schema": "fpl"}

    player_key: Optional[int] = Field(primary_key=True)
    player_id: int = Field(sa_column_kwargs={"nullable": False})
    season: str = Field(sa_column_kwargs={"nullable": False})
    first_name: str = Field(sa_column_kwargs={"nullable": False})
    last_name: str = Field(sa_column_kwargs={"nullable": False})
    web_name: str = Field(sa_column_kwargs={"nullable": False})
    position: str = Field(sa_column_kwargs={"nullable": False})
    price: int = Field(sa_column_kwargs={"nullable": False})
    team_key: int = Field(
        foreign_key="dim_team.team_key",
        sa_column_kwargs={"nullable": False},
    )
    effective_dt: date = Field(sa_column_kwargs={"nullable": False})
    expiry_dt: date = Field(sa_column_kwargs={"nullable": False})
    current_ind: bool = Field(sa_column_kwargs={"nullable": False})


class fact_match_stats(SQLModel, table=True):
    __tablename__ = "fact_match_stats"
    __table_args__ = {"schema": "fpl"}

    extract_dt_key: int = Field(
        foreign_key="dim_date.date_key",
        sa_column_kwargs={"nullable": False},
    )
    player_key: int = Field(
        foreign_key="dim_player.player_key",
        sa_column_kwargs={"nullable": False},
        primary_key=True,
    )
    fixture_key: int = Field(
        foreign_key="dim_fixture.fixture_key",
        sa_column_kwargs={"nullable": False},
        primary_key=True,
    )
    minutes_played: int = Field(sa_column_kwargs={"nullable": False})
    start_ind: int = Field(sa_column_kwargs={"nullable": False})
    total_points: int = Field(sa_column_kwargs={"nullable": False})
    bonus_points: int = Field(sa_column_kwargs={"nullable": False})
    bonus_points_system_value: int = Field(sa_column_kwargs={"nullable": False})
    goals_scored: int = Field(sa_column_kwargs={"nullable": False})
    penalties_missed: int = Field(sa_column_kwargs={"nullable": False})
    expected_goals: float = Field(sa_column_kwargs={"nullable": False})
    assists: int = Field(sa_column_kwargs={"nullable": False})
    expected_assists: float = Field(sa_column_kwargs={"nullable": False})
    expected_goal_involvements: float = Field(sa_column_kwargs={"nullable": False})
    goals_conceded: int = Field(sa_column_kwargs={"nullable": False})
    expected_goals_conceded: float = Field(sa_column_kwargs={"nullable": False})
    own_goals: int = Field(sa_column_kwargs={"nullable": False})
    clean_sheet_ind: int = Field(sa_column_kwargs={"nullable": False})
    saves: int = Field(sa_column_kwargs={"nullable": False})
    penalties_saved: int = Field(sa_column_kwargs={"nullable": False})
    yellow_cards: int = Field(sa_column_kwargs={"nullable": False})
    red_cards: int = Field(sa_column_kwargs={"nullable": False})
    influence: float = Field(sa_column_kwargs={"nullable": False})
    creativity: int = Field(sa_column_kwargs={"nullable": False})
    threat: float = Field(sa_column_kwargs={"nullable": False})
    ict_index: float = Field(sa_column_kwargs={"nullable": False})
    mng_win: int = Field(sa_column_kwargs={"nullable": False})
    mng_draw: int = Field(sa_column_kwargs={"nullable": False})
    mng_loss: int = Field(sa_column_kwargs={"nullable": False})
    mng_underdog_win: int = Field(sa_column_kwargs={"nullable": False})
    mng_underdog_draw: int = Field(sa_column_kwargs={"nullable": False})
    mng_clean_sheets: int = Field(sa_column_kwargs={"nullable": False})
    mng_goals_scored: int = Field(sa_column_kwargs={"nullable": False})
