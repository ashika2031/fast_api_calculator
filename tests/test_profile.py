import pytest
from fastapi import status
from app.models import User


def test_get_current_user_profile(authenticated_client, test_user):
    """Test getting current user's profile."""
    response = authenticated_client.get("/users/me")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert "id" in data
    assert "created_at" in data


def test_get_profile_unauthorized(client):
    """Test getting profile without authentication."""
    response = client.get("/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_user_profile_username(authenticated_client, test_user):
    """Test updating user's username."""
    new_username = "updated_username"
    response = authenticated_client.put(
        "/users/me",
        json={"username": new_username}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == new_username
    assert data["email"] == test_user["email"]


def test_update_user_profile_email(authenticated_client, test_user):
    """Test updating user's email."""
    new_email = "newemail@example.com"
    response = authenticated_client.put(
        "/users/me",
        json={"email": new_email}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == new_email


def test_update_user_profile_both_fields(authenticated_client, test_user):
    """Test updating both username and email."""
    new_username = "completely_new_user"
    new_email = "completelynew@example.com"
    response = authenticated_client.put(
        "/users/me",
        json={"username": new_username, "email": new_email}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == new_username
    assert data["email"] == new_email


def test_update_profile_duplicate_username(authenticated_client, test_user, db_session):
    """Test updating to a username that already exists."""
    # Create another user
    from app.auth import get_password_hash
    another_user = User(
        username="another_user",
        email="another@example.com",
        hashed_password=get_password_hash("password123")
    )
    db_session.add(another_user)
    db_session.commit()
    
    # Try to update to the other user's username
    response = authenticated_client.put(
        "/users/me",
        json={"username": "another_user"}
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already taken" in response.json()["detail"].lower()


def test_update_profile_duplicate_email(authenticated_client, test_user, db_session):
    """Test updating to an email that already exists."""
    # Create another user
    from app.auth import get_password_hash
    another_user = User(
        username="another_user",
        email="another@example.com",
        hashed_password=get_password_hash("password123")
    )
    db_session.add(another_user)
    db_session.commit()
    
    # Try to update to the other user's email
    response = authenticated_client.put(
        "/users/me",
        json={"email": "another@example.com"}
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in response.json()["detail"].lower()


def test_update_profile_unauthorized(client):
    """Test updating profile without authentication."""
    response = client.put(
        "/users/me",
        json={"username": "newname"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_change_password_success(authenticated_client, test_user, client):
    """Test successfully changing password."""
    response = authenticated_client.put(
        "/users/me/password",
        json={
            "current_password": test_user["password"],
            "new_password": "newpassword123"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert "success" in response.json()["message"].lower()
    
    # Verify can login with new password
    login_response = client.post(
        "/users/login",
        json={
            "username": test_user["username"],
            "password": "newpassword123"
        }
    )
    assert login_response.status_code == status.HTTP_200_OK


def test_change_password_incorrect_current(authenticated_client, test_user):
    """Test changing password with incorrect current password."""
    response = authenticated_client.put(
        "/users/me/password",
        json={
            "current_password": "wrongpassword",
            "new_password": "newpassword123"
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "incorrect" in response.json()["detail"].lower()


def test_change_password_unauthorized(client):
    """Test changing password without authentication."""
    response = client.put(
        "/users/me/password",
        json={
            "current_password": "password123",
            "new_password": "newpassword123"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_change_password_weak_password(authenticated_client, test_user):
    """Test changing password to a weak password (less than 6 characters)."""
    response = authenticated_client.put(
        "/users/me/password",
        json={
            "current_password": test_user["password"],
            "new_password": "weak"
        }
    )
    
    # This should fail validation at the Pydantic schema level
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
