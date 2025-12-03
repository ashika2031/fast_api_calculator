import pytest
from fastapi import status


def test_register_user_success(client, test_user):
    """Test successful user registration."""
    response = client.post("/users/register", json=test_user)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data


def test_register_user_duplicate_username(client, test_user):
    """Test registration with duplicate username."""
    # Register first user
    client.post("/users/register", json=test_user)
    
    # Try to register with same username
    response = client.post("/users/register", json=test_user)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Username already registered" in response.json()["detail"]


def test_register_user_duplicate_email(client, test_user, test_user2):
    """Test registration with duplicate email."""
    # Register first user
    client.post("/users/register", json=test_user)
    
    # Try to register with same email but different username
    test_user2["email"] = test_user["email"]
    response = client.post("/users/register", json=test_user2)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]


def test_register_user_invalid_email(client):
    """Test registration with invalid email format."""
    invalid_user = {
        "username": "testuser",
        "email": "not-an-email",
        "password": "password123"
    }
    
    response = client.post("/users/register", json=invalid_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_user_short_password(client):
    """Test registration with password too short."""
    invalid_user = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "123"
    }
    
    response = client.post("/users/register", json=invalid_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_user_success(client, test_user):
    """Test successful user login."""
    # Register user first
    client.post("/users/register", json=test_user)
    
    # Login
    response = client.post("/users/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_wrong_password(client, test_user):
    """Test login with wrong password."""
    # Register user first
    client.post("/users/register", json=test_user)
    
    # Login with wrong password
    response = client.post("/users/login", json={
        "username": test_user["username"],
        "password": "wrongpassword"
    })
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_user_nonexistent(client):
    """Test login with non-existent user."""
    response = client.post("/users/login", json={
        "username": "nonexistent",
        "password": "password123"
    })
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]


def test_user_data_in_database(client, test_user, db_session):
    """Test that user data is correctly stored in database."""
    from app.models import User
    
    # Register user
    response = client.post("/users/register", json=test_user)
    user_id = response.json()["id"]
    
    # Query database
    db_user = db_session.query(User).filter(User.id == user_id).first()
    
    assert db_user is not None
    assert db_user.username == test_user["username"]
    assert db_user.email == test_user["email"]
    assert db_user.hashed_password != test_user["password"]  # Should be hashed
