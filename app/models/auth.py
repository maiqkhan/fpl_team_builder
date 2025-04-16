from ..utils import validate_password
from passlib.context import CryptContext
from sqlmodel import Field, SQLModel
from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    field_validator,
    ValidationInfo,
    AfterValidator,
)
from typing import Optional, Annotated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ValidatePassword = Annotated[SecretStr, AfterValidator(validate_password)]


class UserSignup(BaseModel):
    email: EmailStr
    password: ValidatePassword
    password_confirm: ValidatePassword

    @field_validator("password_confirm", mode="after")
    @classmethod
    def check_passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data["password"]:
            raise ValueError("Passwords do not match")
        return value


class User(SQLModel, table=True):
    __tablename__ = "USERS"
    #__table_args__ = {"schema": "auth"}

    user_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    email: EmailStr = Field(max_length=100)
    password: str = Field(max_length=100)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


class JWTtoken(BaseModel):
    access_token: str
    token_type: str
