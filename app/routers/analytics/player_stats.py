from typing import Annotated
from fastapi import Request, APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlmodel import Session, select
from starlette.authentication import requires

from ... import shortcuts, config, database, oauth2
from ...models import auth as models

settings = config.get_settings()

router = APIRouter(tags=["analytics"])


@router.get("/analytics", response_class=HTMLResponse)
@requires("authenticated", redirect="login")
def analytics_page(request: Request):

    return shortcuts.render(request, "/analytics/stats_page.html", status_code=200)
