import pytest
from fastapi import status
from app.models import User
from app.auth import verify_password


# ==================== UNIT TESTS - Business Logic ====================

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


# ==================== INTEGRATION TESTS - Database Updates ====================

def test_profile_update_persists_in_database(authenticated_client, test_user, db_session):
    """Integration test: Verify profile updates are persisted to database."""
    new_username = "db_updated_user"
    new_email = "dbupdated@example.com"
    
    # Update profile via API
    response = authenticated_client.put(
        "/users/me",
        json={"username": new_username, "email": new_email}
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Query database directly to verify persistence
    user = db_session.query(User).filter(User.username == new_username).first()
    assert user is not None
    assert user.username == new_username
    assert user.email == new_email
    
    # Verify old username no longer exists
    old_user = db_session.query(User).filter(User.username == test_user["username"]).first()
    assert old_user is None


def test_password_change_persists_in_database(authenticated_client, test_user, db_session):
    """Integration test: Verify password change is persisted with proper hashing."""
    new_password = "new_secure_password_123"
    
    # Get user before password change
    user_before = db_session.query(User).filter(User.username == test_user["username"]).first()
    old_hashed_password = user_before.hashed_password
    user_id = user_before.id
    
    # Change password via API
    response = authenticated_client.put(
        "/users/me/password",
        json={
            "current_password": test_user["password"],
            "new_password": new_password
        }
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Query database again for fresh instance
    db_session.commit()  # Ensure any pending changes are flushed
    user_after = db_session.query(User).filter(User.id == user_id).first()
    
    # Verify password was changed (hash is different)
    assert user_after.hashed_password != old_hashed_password
    
    # Verify new password is correctly hashed and verifiable
    assert verify_password(new_password, user_after.hashed_password)
    
    # Verify old password no longer works
    assert not verify_password(test_user["password"], user_after.hashed_password)


def test_profile_update_maintains_data_integrity(authenticated_client, test_user, db_session):
    """Integration test: Verify profile updates don't affect other user data."""
    # Create a calculation for the user first
    calc_response = authenticated_client.post(
        "/calculations/",
        json={"operation": "add", "operand1": 5.0, "operand2": 3.0}
    )
    assert calc_response.status_code == status.HTTP_201_CREATED
    
    # Get user ID
    user = db_session.query(User).filter(User.username == test_user["username"]).first()
    user_id = user.id
    original_created_at = user.created_at
    
    # Update profile
    new_username = "integrity_test_user"
    response = authenticated_client.put(
        "/users/me",
        json={"username": new_username}
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Verify user ID didn't change
    updated_user = db_session.query(User).filter(User.username == new_username).first()
    assert updated_user.id == user_id
    
    # Verify created_at timestamp didn't change
    assert updated_user.created_at == original_created_at
    
    # Verify calculations are still linked to the user
    assert len(updated_user.calculations) == 1
    assert updated_user.calculations[0].user_id == user_id


def test_concurrent_profile_updates_handle_conflicts(client, test_user, db_session):
    """Integration test: Verify duplicate detection works with database constraints."""
    # Create first user
    client.post("/users/register", json=test_user)
    
    # Create second user
    second_user = {
        "username": "second_user",
        "email": "second@example.com",
        "password": "password123"
    }
    client.post("/users/register", json=second_user)
    
    # Login as second user
    login_response = client.post("/users/login", json={
        "username": second_user["username"],
        "password": second_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Try to update second user's username to first user's username
    response = client.put(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": test_user["username"]}
    )
    
    # Should fail due to duplicate username
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    # Verify database still has both users with original usernames
    first_user_db = db_session.query(User).filter(User.username == test_user["username"]).first()
    second_user_db = db_session.query(User).filter(User.username == second_user["username"]).first()
    assert first_user_db is not None
    assert second_user_db is not None
