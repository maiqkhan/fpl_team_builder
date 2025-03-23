from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from . import config, shortcuts
from .routers.auth import users

settings = config.get_settings()

app = FastAPI()

app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
app.include_router(users.router)


@app.get("/")
def home_page(request: Request):
    return shortcuts.render(request, "unauth.html", {}, status_code=200)