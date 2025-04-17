from typing import Annotated
from fastapi import Request, APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlmodel import Session, select
from starlette.authentication import requires

from ... import shortcuts, config

settings = config.get_settings()

router = APIRouter(tags=["analytics"])


@router.get("/build_tool", response_class=HTMLResponse)
@requires("authenticated", redirect="login")
def get_build_tool(request: Request):

    return shortcuts.render(request, "/build_tool/build_page.html", status_code=200)
