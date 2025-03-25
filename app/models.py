
from .database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

class User(Base):
    __tablename__ = "USERS"
    __table_args__ = {"schema": "auth"}

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(60))
    password: Mapped[str] = mapped_column(String(100))

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)