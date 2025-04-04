import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent
    template_dir: Path = Path(__file__).resolve().parent / "templates"
    static_dir: Path = Path(__file__).resolve().parent / "static"
    secret_key: str = Field(..., env="SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    token_expire: int = Field(default=86400, env="TOKEN_EXPIRE")
    db_name: str = Field(..., env="DB_NAME")
    db_server: str = Field(..., env="DB_SERVER")
    db_username: str = Field(..., env="DB_USERNAME")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_port: int = Field(..., env="DB_PORT")

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
