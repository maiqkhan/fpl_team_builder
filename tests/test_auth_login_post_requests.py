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


def test_successful_login_post_request(session: Session, client: TestClient):
    """Test Succesful POST Request to login page"""
    hashed_password = User.get_password_hash(password="Test123!")
    user_account = User(email="test@gmail.com", password=hashed_password)
    session.add(user_account)
    session.commit()

    response = client.post(
        "/login",
        data={
            "username": "test@gmail.com",
            "password": "Test123!",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "session_id" in response.cookies


def test_login_post_request(session: Session, client: TestClient):
    """Test Succesful POST Request to login page"""
    hashed_password = User.get_password_hash(password="Test123!")
    user_account = User(email="test@gmail.com", password=hashed_password)
    session.add(user_account)
    session.commit()

    response = client.post(
        "/login",
        data={
            "username": "test@gmail.com",
            "password": "Test123!",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "session_id" in response.cookies


def test_login_email_nonexistent_post_request(session: Session, client: TestClient):
    """Test Failed POST Request to login page due to email not existing."""
    account_email = "test2@gmail.com"
    hashed_password = User.get_password_hash(password="Test123!")
    user_account = User(email=account_email, password=hashed_password)
    session.add(user_account)
    session.commit()

    response = client.post(
        "/login",
        data={
            "username": "test1@gmail.com",
            "password": "Test123!",
        },
        follow_redirects=False,
    )

    response_dict = response.json()

    assert response.status_code == 401
    assert (
        response_dict["detail"]
        == "Invalid email or password. Please try logging in again."
    )


def test_login_password_nonmatch_post_request(session: Session, client: TestClient):
    """Test Failed POST Request to login page due to email not existing."""
    account_email = "test@gmail.com"
    hashed_password = User.get_password_hash(password="Test123!")
    user_account = User(email=account_email, password=hashed_password)
    session.add(user_account)
    session.commit()

    response = client.post(
        "/login",
        data={
            "username": "test@gmail.com",
            "password": "NonTest123!",
        },
        follow_redirects=False,
    )

    response_dict = response.json()

    assert response.status_code == 401
    assert (
        response_dict["detail"]
        == "Invalid email or password. Please try logging in again."
    )
