from pydantic import SecretStr

# Password policy
SPECIAL_CHARS: set[str] = {
    "$",
    "@",
    "#",
    "%",
    "!",
    "^",
    "&",
    "*",
    "(",
    ")",
    "-",
    "_",
    "+",
    "=",
    "{",
    "}",
    "[",
    "]",
}

MIN_LENGTH: int = 8
MAX_LENGTH: int = 20
INCLUDES_SPECIAL_CHARS: bool = True
INCLUDES_NUMBERS: bool = True
INCLUDES_LOWERCASE: bool = True
INCLUDES_UPPERCASE: bool = True


class PasswordStrength(ValueError):
    message: str


def validate_password(v: SecretStr) -> SecretStr:
    min_length = MIN_LENGTH
    max_length = MAX_LENGTH
    includes_special_chars = INCLUDES_SPECIAL_CHARS
    includes_numbers = INCLUDES_NUMBERS
    includes_lowercase = INCLUDES_LOWERCASE
    includes_uppercase = INCLUDES_UPPERCASE
    special_chars = SPECIAL_CHARS

    if not isinstance(v.get_secret_value(), str):
        raise TypeError("string required")
    if len(v.get_secret_value()) < min_length or len(v.get_secret_value()) > max_length:
        raise PasswordStrength(
            f"Password length should be at least {min_length} characters but not more than {max_length} characters"
        )

    if includes_numbers and not any(char.isdigit() for char in v.get_secret_value()):
        raise PasswordStrength("Password should have at least one numeral")

    if includes_uppercase and not any(char.isupper() for char in v.get_secret_value()):
        raise PasswordStrength("Password should have at least one uppercase letter")

    if includes_lowercase and not any(char.islower() for char in v.get_secret_value()):
        raise PasswordStrength("Password should have at least one lowercase letter")

    if includes_special_chars and not any(
        char in special_chars for char in v.get_secret_value()
    ):
        raise PasswordStrength(f"Password should have at least one special character")

    return v
