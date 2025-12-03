import pytest
from app.database import get_db, engine, Base


def test_get_db_yields_session():
    """Test get_db context manager yields and closes session."""
    db_gen = get_db()
    db = next(db_gen)
    
    # Verify we got a database session
    assert db is not None
    
    # Close the generator (triggers finally block)
    try:
        next(db_gen)
    except StopIteration:
        pass  # Expected


def test_database_engine_and_base():
    """Test database engine and base are properly configured."""
    assert engine is not None
    assert Base is not None
    assert hasattr(Base, 'metadata')
