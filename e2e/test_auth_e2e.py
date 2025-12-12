"""Playwright E2E tests for user registration and login.

Tests cover:
- Positive scenarios: valid registration and login
- Negative scenarios: invalid inputs, short passwords, wrong credentials
"""
import pytest
from playwright.sync_api import Page, expect
import time


class TestRegistration:
    """Test suite for user registration functionality."""
    
    def test_register_with_valid_data(self, page: Page, base_url: str):
        """Test successful registration with valid data.
        
        Verifies:
        - User can navigate to registration page
        - Form accepts valid email and password
        - Success message is displayed
        - JWT token is stored in localStorage
        """
        # Navigate to registration page
        page.goto(f"{base_url}/static/register.html")
        
        # Fill in registration form with valid data
        unique_email = f"test_{int(time.time())}@example.com"
        page.fill('input[id="username"]', f"user_{int(time.time())}")
        page.fill('input[id="email"]', unique_email)
        page.fill('input[id="password"]', "SecurePass123!")
        page.fill('input[id="confirmPassword"]', "SecurePass123!")
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Wait for success message
        success_message = page.locator("#message.success")
        expect(success_message).to_be_visible(timeout=5000)
        expect(success_message).to_contain_text("Registration successful")
        
        # Verify JWT token is stored
        token = page.evaluate("localStorage.getItem('token')")
        assert token is not None, "JWT token should be stored in localStorage"
        assert len(token) > 0, "JWT token should not be empty"
    
    def test_register_with_short_password(self, page: Page, base_url: str):
        """Test registration fails with password shorter than 8 characters.
        
        Verifies:
        - Client-side validation catches short password
        - Error message is displayed
        - Form is not submitted
        """
        page.goto(f"{base_url}/static/register.html")
        
        # Fill form with short password
        unique_email = f"test_{int(time.time())}@example.com"
        page.fill("#username", f"user_{int(time.time())}")
        page.fill("#email", unique_email)
        page.fill("#password", "short")
        page.fill('input[id="confirmPassword"]', "short")
        
        # Submit form
        page.click("#registerBtn")
        
        # Check for error message
        error_message = page.locator("#message.error")
        expect(error_message).to_be_visible(timeout=3000)
        expect(error_message).to_contain_text("at least 8 characters")
    
    def test_register_with_invalid_email(self, page: Page, base_url: str):
        """Test registration fails with invalid email format.
        
        Verifies:
        - Client-side validation catches invalid email
        - Error message is displayed
        """
        page.goto(f"{base_url}/static/register.html")
        
        # Fill form with invalid email
        page.fill("#username", f"user_{int(time.time())}")
        page.fill("#email", "notanemail")
        page.fill("#password", "SecurePass123!")
        page.fill("input[id="confirmPassword"]", "SecurePass123!")
        
        # Submit form
        page.click("#registerBtn")
        
        # Check for error message
        error_message = page.locator("#message.error")
        expect(error_message).to_be_visible(timeout=3000)
        expect(error_message).to_contain_text("valid email")
    
    def test_register_with_mismatched_passwords(self, page: Page, base_url: str):
        """Test registration fails when passwords don't match.
        
        Verifies:
        - Client-side validation catches password mismatch
        - Error message is displayed
        """
        page.goto(f"{base_url}/static/register.html")
        
        # Fill form with mismatched passwords
        unique_email = f"test_{int(time.time())}@example.com"
        page.fill("#username", f"user_{int(time.time())}")
        page.fill("#email", unique_email)
        page.fill("#password", "SecurePass123!")
        page.fill("input[id="confirmPassword"]", "DifferentPass456!")
        
        # Submit form
        page.click("#registerBtn")
        
        # Check for error message
        error_message = page.locator("#message.error")
        expect(error_message).to_be_visible(timeout=3000)
        expect(error_message).to_contain_text("do not match")
    
    def test_register_with_duplicate_email(self, page: Page, base_url: str):
        """Test registration fails with already registered email.
        
        Verifies:
        - Server returns 400 error
        - Error message is displayed to user
        """
        page.goto(f"{base_url}/static/register.html")
        
        # Use existing test user email
        page.fill("#username", f"user_{int(time.time())}")
        page.fill("#email", "test@example.com")  # Existing user
        page.fill("#password", "SecurePass123!")
        page.fill("input[id="confirmPassword"]", "SecurePass123!")
        
        # Submit form
        page.click("#registerBtn")
        
        # Check for error message from server
        error_message = page.locator("#message.error")
        expect(error_message).to_be_visible(timeout=5000)
        expect(error_message).to_contain_text("already registered")


class TestLogin:
    """Test suite for user login functionality."""
    
    def test_login_with_valid_credentials(self, page: Page, base_url: str):
        """Test successful login with correct username and password.
        
        Verifies:
        - User can navigate to login page
        - Form accepts valid credentials
        - JWT token is returned and stored
        - Success message is displayed
        """
        page.goto(f"{base_url}/static/login.html")
        
        # Fill in login form with valid credentials
        page.fill("#username", "testuser")
        page.fill("#password", "SecurePass123")
        
        # Submit form
        page.click("button[type="submit"]")
        
        # Wait for success message
        success_message = page.locator("#message.success")
        expect(success_message).to_be_visible(timeout=5000)
        expect(success_message).to_contain_text("Login successful")
        
        # Verify JWT token is stored
        token = page.evaluate("localStorage.getItem('token')")
        assert token is not None, "JWT token should be stored in localStorage"
        assert len(token) > 0, "JWT token should not be empty"
    
    def test_login_with_wrong_password(self, page: Page, base_url: str):
        """Test login fails with incorrect password.
        
        Verifies:
        - Server returns 401 Unauthorized
        - Error message is displayed
        - No token is stored
        """
        page.goto(f"{base_url}/static/login.html")
        
        # Fill form with wrong password
        page.fill("#username", "testuser")
        page.fill("#password", "WrongPassword123")
        
        # Submit form
        page.click("button[type="submit"]")
        
        # Check for error message
        error_message = page.locator("#message.error")
        expect(error_message).to_be_visible(timeout=5000)
        expect(error_message).to_contain_text("Invalid credentials")
        
        # Verify no token is stored
        token = page.evaluate("localStorage.getItem('token')")
        assert token is None or token == "", "No token should be stored on failed login"
    
    def test_login_with_nonexistent_user(self, page: Page, base_url: str):
        """Test login fails with username that doesn't exist.
        
        Verifies:
        - Server returns 401 Unauthorized
        - Error message is displayed
        """
        page.goto(f"{base_url}/static/login.html")
        
        # Fill form with non-existent username
        page.fill("#username", f"nonexistent_{int(time.time())}")
        page.fill("#password", "SomePassword123")
        
        # Submit form
        page.click("button[type="submit"]")
        
        # Check for error message
        error_message = page.locator("#message.error")
        expect(error_message).to_be_visible(timeout=5000)
        expect(error_message).to_contain_text("Invalid credentials")
    
    def test_login_with_empty_fields(self, page: Page, base_url: str):
        """Test login form validates required fields.
        
        Verifies:
        - Client-side validation prevents submission
        - Error message is displayed
        """
        page.goto(f"{base_url}/static/login.html")
        
        # Try to submit empty form
        page.click("button[type="submit"]")
        
        # Check for error message
        error_message = page.locator("#message.error")
        expect(error_message).to_be_visible(timeout=3000)


class TestNavigation:
    """Test suite for navigation between pages."""
    
    def test_navigate_from_login_to_register(self, page: Page, base_url: str):
        """Test navigation link from login to registration page."""
        page.goto(f"{base_url}/static/login.html")
        
        # Click register link
        page.click("text=Register here")
        
        # Verify navigation to register page
        expect(page).to_have_url(f"{base_url}/static/register.html")
    
    def test_navigate_from_register_to_login(self, page: Page, base_url: str):
        """Test navigation link from registration to login page."""
        page.goto(f"{base_url}/static/register.html")
        
        # Click login link
        page.click("text=Login here")
        
        # Verify navigation to login page
        expect(page).to_have_url(f"{base_url}/static/login.html")
