from typing import Annotated
from fastapi import Request, APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlmodel import Session, select

from ... import shortcuts, config, database, models, oauth2

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


@router.get("/login", response_class=HTMLResponse, name="login")
def login_page(request: Request):

    if "session_id" in request.cookies:
        return shortcuts.redirect("/", cookies=request.cookies)
    else:
        return shortcuts.render(request, "/auth/login.html", status_code=200)


@router.post("/login", response_class=HTMLResponse)
def login_user(
    request: Request,
    session: SessionDep,
    user_credentials: OAuth2PasswordRequestForm = Depends(),
):

    user_account = session.exec(
        select(models.User).where(models.User.email == user_credentials.username)
    ).first()

    if not user_account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account doesn't exist. Please try logging in again.",
        )

    if not models.User.verify_password(
        user_credentials.password, user_account.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. Please try logging in again.",
        )

    access_token = oauth2.create_access_token(
        data={"user_id": user_account.user_id}, expires_delta=settings.token_expire
    )

    return shortcuts.redirect("/", cookies={"session_id": access_token})


@router.get("/signup", response_class=HTMLResponse)
def signin_page(request: Request):

    if "session_id" in request.cookies:
        return shortcuts.redirect("/", cookies=request.cookies)
    else:
        return shortcuts.render(request, "/auth/signup.html", status_code=200)


@router.post("/signup", response_class=HTMLResponse)
def register_user(
    request: Request,
    session: SessionDep,
    user_credentials: OAuth2PasswordSignupForm = Depends(),
):

    try:
        user_account = models.UserSignup(
            email=user_credentials.username,
            password=user_credentials.password,
            password_confirm=user_credentials.reconfirmPassword,
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e.errors()[0]['msg']}",
        ) from e

    if session.exec(
        select(models.User).where(models.User.email == user_account.email)
    ).first():

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{user_account.email} is not available. Please pick another email.",
        )

    password_hash = models.User.get_password_hash(
        user_account.password.get_secret_value()
    )

    try:
        user = models.User(email=user_account.email, password=password_hash)

        session.add(user)
        session.commit()
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e.errors()[0]['ctx']['error']}.",
        ) from e

    user_account = session.exec(
        select(models.User).where(models.User.email == user_account.email)
    ).first()

    access_token = oauth2.create_access_token(
        data={"user_id": user_account.user_id}, expires_delta=settings.token_expire
    )

    return shortcuts.redirect("/", cookies={"session_id": access_token})


@router.get("/logout", response_class=HTMLResponse)
def logout_page(request: Request):

    return shortcuts.redirect("/", cookies={}, remove_session=True)
