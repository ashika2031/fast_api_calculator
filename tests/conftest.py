import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.config import settings
import os

# Use SQLite for testing if PostgreSQL is not available
if os.getenv("USE_SQLITE_FOR_TESTS", "true").lower() == "true":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/test_calculator_db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user():
    """Test user data."""
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123"
    }


@pytest.fixture
def test_user2():
    """Second test user data."""
    return {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password": "testpassword456"
    }


@pytest.fixture
def authenticated_client(client, test_user):
    """Create an authenticated test client."""
    # Register user
    client.post("/users/register", json=test_user)
    
    # Login and get token
    response = client.post("/users/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = response.json()["access_token"]
    
    # Set authorization header
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client
