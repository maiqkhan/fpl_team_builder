from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.middleware.authentication import AuthenticationMiddleware
from sqlmodel import SQLModel, select, desc
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from . import config, shortcuts, backends, database
from .routers.auth import users
from .routers.analytics import player_stats
from .routers.build_tool import build_tool
from .models.analytics import GameweekDeadline, FormPlayers, KeyFixtures, PriceChanges
from .models.auth import User

settings = config.get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for the Team Builder app."""
    # Initialize the database connection pool
    SQLModel.metadata.create_all(bind=database.engine)
    yield
    # Close the database connection pool


app = FastAPI(lifespan=lifespan)

app.add_middleware(AuthenticationMiddleware, backend=backends.JWTCookieBackend())
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
app.include_router(users.router)
app.include_router(player_stats.router)
app.include_router(build_tool.router)


@app.get("/")
def home_page(request: Request, session: database.SessionDep):

    if request.user.is_authenticated:

        # Check if the user is authenticated
        upcoming_deadline = session.exec(
            select(GameweekDeadline)
            .where(GameweekDeadline.deadline >= datetime.now(timezone.utc))
            .order_by(GameweekDeadline.deadline)
        ).first()

        deadline_utc = (
            upcoming_deadline.deadline.isoformat() + "Z" if upcoming_deadline else None
        )

        form_players = session.exec(
            select(FormPlayers).order_by(desc(FormPlayers.form)).limit(5)
        )

        form_player_lst = [dict(player) for player in form_players.fetchall()]

        key_fixtures = session.exec(
            select(KeyFixtures).order_by(desc(KeyFixtures.ownership_score)).limit(5)
        )

        key_fixture_lst = [dict(fixture) for fixture in key_fixtures.fetchall()]

        price_changes = session.exec(
            select(PriceChanges).order_by(desc(PriceChanges.price_change_date)).limit(5)
        )

        price_changes_lst = [
            dict(price_change) for price_change in price_changes.fetchall()
        ]

        return shortcuts.render(
            request,
            "dashboard.html",
            {
                "nextDeadline": deadline_utc,
                "nextGameweek": upcoming_deadline.gameweek,
                "form_players": form_player_lst,
                "key_fixtures": key_fixture_lst,
                "price_changes": price_changes_lst,
            },
            status_code=200,
        )
    else:
        return shortcuts.render(request, "unauth.html", {}, status_code=200)
