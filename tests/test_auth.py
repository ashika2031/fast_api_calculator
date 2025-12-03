import pytest
from fastapi import status
from app.auth import get_current_user, create_access_token
from datetime import timedelta
from jose import jwt
from app.config import settings


def test_get_current_user_invalid_token(client, db_session):
    """Test get_current_user with invalid token."""
    from fastapi import HTTPException
    from app.database import get_db
    
    # Test with invalid token
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token="invalid_token", db=db_session)
    
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_no_username_in_token(client, db_session):
    """Test get_current_user with token missing username."""
    from fastapi import HTTPException
    
    # Create token without 'sub' claim
    token = create_access_token(data={"user_id": 123})
    
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token=token, db=db_session)
    
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_nonexistent_user(client, db_session):
    """Test get_current_user with valid token but nonexistent user."""
    from fastapi import HTTPException
    
    # Create token for nonexistent user
    token = create_access_token(data={"sub": "nonexistent_user"})
    
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token=token, db=db_session)
    
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_access_token_with_custom_expiry():
    """Test creating access token with custom expiration time."""
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=60)
    
    token = create_access_token(data=data, expires_delta=expires_delta)
    
    # Decode and verify
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload.get("sub") == "testuser"
    assert "exp" in payload


def test_create_access_token_without_expiry():
    """Test creating access token without custom expiration (uses default)."""
    data = {"sub": "testuser"}
    
    token = create_access_token(data=data)
    
    # Decode and verify
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload.get("sub") == "testuser"
    assert "exp" in payload
