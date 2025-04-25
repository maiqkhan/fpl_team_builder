from typing import Annotated
from fastapi import Request, APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlmodel import Session, select
from starlette.authentication import requires
from ... import shortcuts, config, database, oauth2
from sqlmodel import Session, select, desc, func
from datetime import datetime as dt
from sqlalchemy.sql import func as sa_func

from ...models import build_tool as models

settings = config.get_settings()

router = APIRouter(tags=["analytics"])


@router.get("/analytics", response_class=HTMLResponse)
@requires("authenticated", redirect="login")
def analytics_page(
    request: Request,
    session: database.SessionDep,
):

    recently_completed_gameweek = session.exec(
        select(models.dim_fixture.gameweek)
        .group_by(models.dim_fixture.gameweek)
        .having(func.max(models.dim_fixture.kickoff_time) < func.now())
        .order_by(desc(models.dim_fixture.gameweek))
    ).first()

    player_stats = session.exec(
        select(
            models.dim_player.web_name,
            models.dim_player.position,
            models.dim_team.short_name,
            func.sum(models.fact_match_stats.total_points).label("points"),
            func.sum(models.fact_match_stats.bonus_points).label("bonus"),
            func.sum(models.fact_match_stats.bonus_points_system_value).label(
                "bonus_PS"
            ),
            func.sum(models.fact_match_stats.goals_scored).label("goals_scored"),
            func.sum(models.fact_match_stats.assists).label("assists"),
            func.sum(
                models.fact_match_stats.goals_scored + models.fact_match_stats.assists
            ).label("goal_contributions"),
            func.sum(models.fact_match_stats.expected_goals).label("expected_goals"),
            func.sum(models.fact_match_stats.expected_assists).label(
                "expected_assists"
            ),
            func.sum(models.fact_match_stats.expected_goal_involvements).label(
                "expected_goal_involvements"
            ),
            func.sum(models.fact_match_stats.clean_sheet_ind).label("clean_sheets"),
            func.sum(models.fact_match_stats.yellow_cards).label("yellow_cards"),
            func.sum(models.fact_match_stats.saves).label("saves"),
        )
        .join(
            models.dim_fixture,
            models.dim_fixture.fixture_key == models.fact_match_stats.fixture_key,
        )
        .join(
            models.dim_player,
            models.dim_player.player_key == models.fact_match_stats.player_key,
        )
        .join(models.dim_team, models.dim_team.team_key == models.dim_player.team_key)
        .where(
            models.dim_fixture.gameweek.between(
                recently_completed_gameweek - 4, recently_completed_gameweek
            ),
            models.dim_player.position != "Manager",
        )
        .group_by(
            models.dim_player.player_key,
            models.dim_player.position,
            models.dim_team.short_name,
        )
        .order_by(desc(func.sum(models.fact_match_stats.total_points)))
        .limit(50)
    ).all()

    current_teams = session.exec(
        select(models.dim_team.short_name)
        .order_by(desc(models.dim_team.team_key))
        .limit(20)
    )

    team_list = sorted(current_teams.all())

    return shortcuts.render(
        request,
        "/analytics/stats_page.html",
        context={"player_data": player_stats, "teams": team_list},
        status_code=200,
    )
