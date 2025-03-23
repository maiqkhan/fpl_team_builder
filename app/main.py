from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from . import config, shortcuts

settings = config.get_settings()

app = FastAPI()

app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")


@app.get("/")
def home_page(request: Request):
    return shortcuts.render(request, "unauth.html", {}, status_code=200)

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return shortcuts.render(request, "/auth/login.html", status_code=200)

@app.get("/signup", response_class=HTMLResponse)
def login_page(request: Request):

    return shortcuts.render(request, "/auth/signup.html", status_code=200)