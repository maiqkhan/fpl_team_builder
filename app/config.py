from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent 
    template_dir: Path = Path(__file__).resolve().parent / "templates"
    static_dir: Path = Path(__file__).resolve().parent / "static"

@lru_cache
def get_settings():
    return Settings()