from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_login_route():
    """Test GET request to login route with no cookies"""
    response = client.get("/login")
    print(response.url)
    assert response.status_code == 200
    assert response.cookies == {}


def test_get_login_route_with_session_cookie():
    """Test GET request to login route with session_id cookie"""
    test_client = TestClient(app, cookies={"session_id": "test_cookie"})
    response = test_client.get("/login")
    assert response.url == "http://testserver/"
    assert response.status_code == 200


def test_get_signup_route():
    """Test GET request to signup route"""
    response = client.get("/signup")
    assert response.status_code == 200
    assert response.cookies == {}


def test_get_signup_route_with_session_cookie():
    """Test GET request to signup route with session_id cookie"""
    test_client = TestClient(app, cookies={"session_id": "test_cookie"})
    response = test_client.get("/signup")
    assert response.url == "http://testserver/"
    assert response.status_code == 200
