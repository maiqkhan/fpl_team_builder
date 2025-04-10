from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.middleware.authentication import AuthenticationMiddleware

from . import config, shortcuts, backends
from .routers.auth import users


# models.Base.metadata.create_all(bind=database.engine)

settings = config.get_settings()

app = FastAPI()

app.add_middleware(AuthenticationMiddleware, backend=backends.JWTCookieBackend())
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
app.include_router(users.router)


@app.get("/")
def home_page(request: Request):

    if request.user.is_authenticated:
        return shortcuts.render(request, "dashboard.html", {}, status_code=200)
    else:
        return shortcuts.render(request, "unauth.html", {}, status_code=200)
