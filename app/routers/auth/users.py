from typing import Annotated
from fastapi import Request, APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from ... import shortcuts, config, database, models, auth

settings = config.get_settings()

router = APIRouter(tags=["authentication"])

SessionDep = Annotated[Session, Depends(database.get_session)]


class OAuth2PasswordSignupForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
        reconfirmPassword: str = Form(...),
    ):
        super().__init__(username=username, password=password, scope="")
        self.reconfirmPassword = reconfirmPassword


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return shortcuts.render(request, "/auth/login.html", status_code=200)


@router.get("/signup", response_class=HTMLResponse)
def signin_page(request: Request):

    return shortcuts.render(request, "/auth/signup.html", status_code=200)


@router.post("/signup", response_class=HTMLResponse)
def register_user(
    request: Request,
    session: SessionDep,
    user_credentials: OAuth2PasswordSignupForm = Depends(),
):

    user_account = models.UserSignup(
        email=user_credentials.username,
        password=user_credentials.password,
        password_confirm=user_credentials.reconfirmPassword,
    )

    if session.exec(
        select(models.User).where(models.User.email == user_account.email)
    ).first():
        raise ValueError(
            f"{user_account.email} is not available. Please pick another email."
        )

    password_hash = auth.get_password_hash(user_account.password.get_secret_value())

    user = models.User(email=user_account.email, password=password_hash)

    session.add(user)
    session.commit()

    # Check that email doesn't exist in users table DONE
    # Check that email matches pattern of an email  DONE
    # Check that password and reconfirm password matches DONE
    # Check that password is strong - meets certain requirements DONE
    # Hash password
