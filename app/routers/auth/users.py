from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse


from ... import shortcuts, config

settings = config.get_settings()

router = APIRouter(
    tags=["authentication"]
)

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return shortcuts.render(request, "/auth/login.html", status_code=200)

@router.get("/signup", response_class=HTMLResponse)
def login_page(request: Request):

    return shortcuts.render(request, "/auth/signup.html", status_code=200)