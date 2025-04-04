# from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings
from sqlmodel import Session, create_engine

settings = get_settings()

engine = create_engine(
    f"postgresql+psycopg2://{settings.db_username}:{settings.db_password}@{settings.db_server}:{settings.db_port}/{settings.db_name}"
)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


def get_session():
    with Session(engine) as session:
        yield session
