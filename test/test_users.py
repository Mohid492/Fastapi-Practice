from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import get_db
from app.schemas import *
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base

# Use a dedicated test database
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/post_db_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test1@test.com", "password": "test"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    # Return the user data so it can be used in tests
    new_user = res.json()
    new_user["password"] = user_data["password"]  # Add password since it's not returned
    return new_user

@pytest.fixture
def token(client, test_user):
    login_res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    assert login_res.status_code == 200
    token = login_res.json().get("access_token")
    return token

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture #scope=module/session
def session():
    # Drop and recreate all tables for a clean slate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Create a fresh session for the test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    # Override the dependency to use our test session
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Create test client
    test_client = TestClient(app)
    yield test_client

    # Clean up after test
    app.dependency_overrides.clear()


def test_create_user(client):
    res = client.post("/users/", json={"email": "test@test.com", "password": "test"})
    new_user = UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == "test@test.com"


def test_create_post(authorized_client):
    post_data = {
        "title": "Anime",
        "content": "Anime content",
        "published": True
    }

    response = authorized_client.post("/posts/", json=post_data)
    assert response.status_code == 201

    data = response.json()
    assert data["published"] == True
    assert "id" in data
    assert data["owner_id"] is not None

@pytest.fixture
def sample_post(authorized_client):
    post_data = {
        "title": "Anime",
        "content": "Anime content",
        "published": True
    }
    response = authorized_client.post("/posts/", json=post_data)
    assert response.status_code == 201
    return response.json()

def test_vote_on_post(authorized_client,sample_post):
    res=authorized_client.post('/votes/',json={"post_id":sample_post["id"],"dir": 1})
    assert res.status_code==201