from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
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
    """Test Succesfull POST Request to signup page"""
    response = client.post(
        "/signup",
        data={
            "username": "test@gmail.com",
            "password": "Abcd123!",
            "reconfirmPassword": "Abcd123!",
        },
    )
    print(response.status_code)
    assert response.status_code == 200
