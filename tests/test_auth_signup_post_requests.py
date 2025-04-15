from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.models.auth import User
import json
from app.database import get_session
import pytest

base_client = TestClient(app)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_successful_signup_post_request(client: TestClient):
    """Test Succesful POST Request to signup page"""
    response = client.post(
        "/signup",
        data={
            "username": "test@gmail.com",
            "password": "Abcd123!",
            "reconfirmPassword": "Abcd123!",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "session_id" in response.cookies


def test_signup_invalid_email_post_request(client: TestClient):
    """Test Failed POST Request to signup page from invalid email"""
    response = client.post(
        "/signup",
        data={
            "username": "testgmail.com",
            "password": "Abcd123!",
            "reconfirmPassword": "Abcd123!",
        },
    )
    response_dict = response.json()

    assert response.status_code == 400
    assert (
        response_dict["detail"]
        == "value is not a valid email address: An email address must have an @-sign."
    )


def test_signup_password_length_le8_post_request(client: TestClient):
    """Test Failed POST Request to signup page due to password less than 8 characters."""
    response = client.post(
        "/signup",
        data={
            "username": "test@gmail.com",
            "password": "Abcd12!",
            "reconfirmPassword": "Abcd12!",
        },
    )
    response_dict = response.json()

    assert response.status_code == 400
    assert (
        response_dict["detail"]
        == "Value error, Password length should be at least 8 characters but not more than 20 characters"
    )


def test_signup_password_length_gr20_post_request(client: TestClient):
    """Test Failed POST Request to signup page due to password more than 20 characters."""
    response = client.post(
        "/signup",
        data={
            "username": "test@gmail.com",
            "password": "Abcdefghij1234567890!",
            "reconfirmPassword": "Abcdefghij1234567890!",
        },
    )
    response_dict = response.json()

    assert response.status_code == 400
    assert (
        response_dict["detail"]
        == "Value error, Password length should be at least 8 characters but not more than 20 characters"
    )


def test_signup_password_no_numbers_post_request(client: TestClient):
    """Test Failed POST Request to signup page due to no numbers in password."""
    response = client.post(
        "/signup",
        data={
            "username": "test@gmail.com",
            "password": "Abcdefg!",
            "reconfirmPassword": "Abcdefg!",
        },
    )
    response_dict = response.json()

    assert response.status_code == 400
    assert (
        response_dict["detail"]
        == "Value error, Password should have at least one numeral"
    )


def test_signup_password_no_uppercase_char_post_request(client: TestClient):
    """Test Failed POST Request to signup page due to no uppercase characters in password."""
    response = client.post(
        "/signup",
        data={
            "username": "test@gmail.com",
            "password": "abcdefg1!",
            "reconfirmPassword": "abcdefg1!",
        },
    )
    response_dict = response.json()

    assert response.status_code == 400
    assert (
        response_dict["detail"]
        == "Value error, Password should have at least one uppercase letter"
    )


def test_signup_password_no_lowercase_char_post_request(client: TestClient):
    """Test Failed POST Request to signup page due to no lowercase characters in password."""
    response = client.post(
        "/signup",
        data={
            "username": "test@gmail.com",
            "password": "ABCD123!",
            "reconfirmPassword": "ABCD123!",
        },
    )
    response_dict = response.json()

    assert response.status_code == 400
    assert (
        response_dict["detail"]
        == "Value error, Password should have at least one lowercase letter"
    )


def test_signup_password_no_special_char_post_request(client: TestClient):
    """Test Failed POST Request to signup page due to no special characters in password."""
    response = client.post(
        "/signup",
        data={
            "username": "test@gmail.com",
            "password": "Abcd1234",
            "reconfirmPassword": "Abcd1234",
        },
    )
    response_dict = response.json()

    assert response.status_code == 400
    assert (
        response_dict["detail"]
        == "Value error, Password should have at least one special character"
    )


## add one for where email already exists
def test_signup_password_taken_email_request(session: Session, client: TestClient):
    """Test Failed POST Request to signup page due to email already taken."""
    account_email = "test@gmail.com"
    hashed_password = User.get_password_hash(password="Test123!")
    user_account = User(email=account_email, password=hashed_password)
    session.add(user_account)
    session.commit()

    response = client.post(
        "/signup",
        data={
            "username": account_email,
            "password": "Test123!",
            "reconfirmPassword": "Test123!",
        },
        follow_redirects=False,
    )

    response_dict = response.json()

    assert response.status_code == 401
    assert (
        response_dict["detail"]
        == f"{account_email} is not available. Please pick another email."
    )
