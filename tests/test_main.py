from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token():
    client.post("/register", json={"username": "testuser", "password": "testpass123"})
    response = client.post("/login", json={"username": "testuser", "password": "testpass123"})
    return response.json()["access_token"]


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Movie Database API is running"


def test_register():
    response = client.post("/register", json={"username": "user1", "password": "pass123"})
    assert response.status_code in [200, 400]


def test_login():
    client.post("/register", json={"username": "loginuser", "password": "pass123"})
    response = client.post("/login", json={"username": "loginuser", "password": "pass123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_movie():
    token = get_token()
    response = client.post(
        "/movies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Inception",
            "director": "Christopher Nolan",
            "genre": "Sci-Fi",
            "year": 2010,
            "rating": 8.8
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Inception"


def test_get_movies():
    token = get_token()
    response = client.get("/movies", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)