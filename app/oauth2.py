from datetime import timedelta, datetime as dt
import jwt

from . import config

settings = config.get_settings()


def create_access_token(data: dict, expires_delta: timedelta = 15):

    expire = dt.now() + timedelta(expires_delta)

    data_encoded = data.copy()
    data_encoded.update({"exp": expire})

    encoded_jwt = jwt.encode(
        data_encoded, key=settings.secret_key, algorithm=settings.jwt_algorithm
    )

    return encoded_jwt
