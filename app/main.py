from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.middleware.authentication import AuthenticationMiddleware
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

from . import config, shortcuts, backends, database
from .routers.auth import users
from .models.analytics import GameweekDeadline
from .models.auth import User

settings = config.get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for the Team Builder app."""
    # Initialize the database connection pool
    SQLModel.metadata.create_all(bind=database.engine)
    yield
    # Close the database connection pool
    await database.engine.dispose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(AuthenticationMiddleware, backend=backends.JWTCookieBackend())
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
app.include_router(users.router)


@app.get("/")
def home_page(request: Request, session: database.SessionDep):

    if request.user.is_authenticated:

        # Check if the user is authenticated

        return shortcuts.render(request, "dashboard.html", {}, status_code=200)
    else:
        return shortcuts.render(request, "unauth.html", {}, status_code=200)
