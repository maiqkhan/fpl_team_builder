import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent
    template_dir: Path = Path(__file__).resolve().parent / "templates"
    static_dir: Path = Path(__file__).resolve().parent / "static"

    secret_key: str = Field()
    jwt_algorithm: str = Field(default="HS256")
    token_expire: int = Field(default=86400)
    db_name: str = Field()
    db_server: str = Field()
    db_username: str = Field()
    db_password: str = Field()
    db_port: int = Field()

    model_config = SettingsConfigDict(env_file=".env", env_prefix="")


@lru_cache
def get_settings():
    return Settings()
