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


@pytest.fixture
def authenticated_page(page, unique_email):
    """Create an authenticated page by registering and logging in a test user."""
    # Register a new test user
    page.goto("http://localhost:8000/static/register.html")
    
    username = f"testuser_{int(unique_email.split('_')[1].split('@')[0])}"
    
    page.fill("#username", username)
    page.fill("#email", unique_email)
    page.fill("#password", "testpass123")
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
    
    # Wait a bit for registration to complete
    page.wait_for_timeout(1000)
    
    # Login with the same user
    page.goto("http://localhost:8000/static/login.html")
    page.wait_for_load_state("networkidle")
    
    page.fill("#username", username)
    page.fill("#password", "testpass123")
    page.click("button[type='submit']")
    
    # Wait for the redirect to calculations page
    page.wait_for_url("http://localhost:8000/static/calculations.html", timeout=10000)
    page.wait_for_load_state("networkidle")
    
    return page

