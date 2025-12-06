"""Playwright E2E test configuration."""
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application."""
    return "http://localhost:8000"


@pytest.fixture
def unique_email():
    """Generate unique email for each test."""
    import time
    return f"test_{int(time.time())}@example.com"
