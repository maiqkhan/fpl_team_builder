from datetime import timedelta, datetime as dt
from jwt import PyJWTError, encode, decode, ExpiredSignatureError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from . import config

settings = config.get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: timedelta = 15):

    expire = dt.now() + timedelta(expires_delta)

    data_encoded = data.copy()
    data_encoded.update({"exp": expire})

    encoded_jwt = encode(
        data_encoded, key=settings.secret_key, algorithm=settings.jwt_algorithm
    )

    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            token, key=settings.secret_key, algorithms=[settings.jwt_algorithm]
        )

        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except ExpiredSignatureError:
        return None
    except PyJWTError:
        return None

    return user_id
