"""
E2E tests for user profile management functionality.
Tests complete user flows: login → profile → update → logout → re-login
"""
import pytest
import time


def wait_for_profile_success(page):
    """Helper function to wait for profile update success message."""
    page.wait_for_function(
        "document.querySelector('#profileMessage').style.display === 'block' && document.querySelector('#profileMessage').classList.contains('success')",
        timeout=10000
    )


def wait_for_password_success(page):
    """Helper function to wait for password change success message."""
    page.wait_for_function(
        "document.querySelector('#passwordMessage').style.display === 'block' && document.querySelector('#passwordMessage').classList.contains('success')",
        timeout=10000
    )


@pytest.fixture
def authenticated_page(page):
    """Create a user account and return authenticated page."""
    timestamp = int(time.time() * 1000)
    username = f"profile_user_{timestamp}"
    email = f"profile_user_{timestamp}@example.com"
    password = "testpassword123"
    
    # Navigate to registration page
    page.goto("http://localhost:8000/static/register.html")
    
    # Register new user
    page.fill("input[name='username']", username)
    page.fill("input[name='email']", email)
    page.fill("input[name='password']", password)
    page.fill("input[id='confirmPassword']", password)
    page.click("button[type='submit']")
    
    # Wait for redirect to login page
    page.wait_for_url("**/login.html", timeout=5000)
    
    # Login with new credentials
    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)
    page.click("button[type='submit']")
    
    # Wait for redirect to calculations page
    page.wait_for_url("**/calculations.html", timeout=5000)
    
    return page, {"username": username, "email": email, "password": password}


class TestProfilePageAccess:
    """Test accessing the profile page."""
    
    def test_profile_page_accessible_from_dashboard(self, authenticated_page):
        """E2E: Access profile page from calculator dashboard."""
        page, user_data = authenticated_page
        
        # Verify we're on calculations page
        assert "calculations.html" in page.url
        
        # Click profile button
        page.click('a.profile-btn')
        
        # Wait for profile page to load
        page.wait_for_url("**/profile.html", timeout=5000)
        
        # Verify profile page loaded
        assert "profile.html" in page.url
        assert page.locator("h1:has-text('User Profile')").is_visible()
    
    def test_profile_page_redirects_if_not_authenticated(self, page):
        """E2E: Verify profile page redirects to login if not authenticated."""
        # Try to access profile page without authentication
        page.goto("http://localhost:8000/static/profile.html")
        
        # Should redirect to login page
        page.wait_for_url("**/login.html", timeout=5000)
        assert "login.html" in page.url


class TestProfileDisplay:
    """Test profile information display."""
    
    def test_current_profile_information_displayed(self, authenticated_page):
        """E2E: Verify current profile information is correctly displayed."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_load_state("networkidle")
        
        # Verify username is displayed
        username_element = page.locator("#currentUsername")
        assert username_element.inner_text() == user_data["username"]
        
        # Verify email is displayed
        email_element = page.locator("#currentEmail")
        assert email_element.inner_text() == user_data["email"]
        
        # Verify member since date is displayed
        member_since_element = page.locator("#memberSince")
        assert member_since_element.inner_text() != "Loading..."
    
    def test_profile_form_placeholders_match_current_data(self, authenticated_page):
        """E2E: Verify form placeholders show current username and email."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_load_state("networkidle")
        
        # Check username placeholder
        username_input = page.locator("#username")
        assert username_input.get_attribute("placeholder") == user_data["username"]
        
        # Check email placeholder
        email_input = page.locator("#email")
        assert email_input.get_attribute("placeholder") == user_data["email"]


class TestProfileUpdate:
    """Test updating profile information."""
    
    def test_update_username_requires_relogin(self, authenticated_page):
        """E2E: Update username causes logout (token invalidation)."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_load_state("networkidle")
        
        # Update username
        new_username = f"{user_data['username']}_updated"
        page.fill("#username", new_username)
        page.click("#updateProfileBtn")
        
        # Should redirect to login after username change (token becomes invalid)
        page.wait_for_url("**/login.html", timeout=10000)
        assert "login.html" in page.url
    
    def test_update_email_success(self, authenticated_page):
        """E2E: Update email and verify changes persist."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_load_state("networkidle")
        
        # Update email
        new_email = f"updated_{user_data['email']}"
        page.fill("#email", new_email)
        page.click("#updateProfileBtn")
        
        # Wait for success message
        wait_for_profile_success(page)
        
        # Verify email updated in display
        page.wait_for_timeout(1000)
        assert page.locator("#currentEmail").inner_text() == new_email
    
    def test_update_both_username_and_email_causes_logout(self, authenticated_page):
        """E2E: Update both username and email causes logout (token invalidation)."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_load_state("networkidle")
        
        # Update both fields (username change will invalidate token)
        new_username = f"{user_data['username']}_both"
        new_email = f"both_{user_data['email']}"
        
        page.fill("#username", new_username)
        page.fill("#email", new_email)
        page.click("#updateProfileBtn")
        
        # Should redirect to login after username change
        page.wait_for_url("**/login.html", timeout=10000)
        assert "login.html" in page.url
        
    def test_update_profile_with_empty_fields_shows_error(self, authenticated_page):
        """E2E: Try to update profile without entering any data."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_load_state("networkidle")
        
        # Click update without filling fields
        page.click("#updateProfileBtn")
        
        # Should show error message
        page.wait_for_selector(".message.error", timeout=5000)
        error_message = page.locator(".message.error")
        assert error_message.is_visible()


class TestPasswordChange:
    """Test password change functionality."""
    
    def test_change_password_success(self, authenticated_page):
        """E2E: Change password and verify can login with new password."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_load_state("networkidle")
        
        # Change password
        new_password = "new_secure_password_456"
        page.fill("#currentPassword", user_data["password"])
        page.fill("#newPassword", new_password)
        page.fill("#confirmPassword", new_password)
        page.click("#changePasswordBtn")
        
        # Wait for success message
        page.wait_for_selector("#passwordMessage.success", timeout=5000)
        success_message = page.locator("#passwordMessage.success")
        assert success_message.is_visible()
        assert "success" in success_message.inner_text().lower()
        
        # Logout
        page.click("#logoutBtn")
        page.wait_for_url("**/login.html", timeout=5000)
        
        # Try to login with NEW password
        page.fill("input[name='username']", user_data["username"])
        page.fill("input[name='password']", new_password)
        page.click("button[type='submit']")
        
        # Should successfully login and redirect to calculations
        page.wait_for_url("**/calculations.html", timeout=5000)
        assert "calculations.html" in page.url
    
    def test_change_password_with_wrong_current_password(self, authenticated_page):
        """E2E: Try to change password with incorrect current password."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_load_state("networkidle")
        
        # Try to change password with wrong current password
        page.fill("#currentPassword", "wrong_password")
        page.fill("#newPassword", "new_password_123")
        page.fill("#confirmPassword", "new_password_123")
        page.click("#changePasswordBtn")
        
        # Should show error message
        page.wait_for_selector('#passwordMessage[style*="display: block"].error', timeout=5000)
        error_message = page.locator("#passwordMessage.error")
        assert error_message.is_visible()
        assert "incorrect" in error_message.inner_text().lower()
    
    def test_change_password_with_mismatched_confirmation(self, authenticated_page):
        """E2E: Try to change password with mismatched confirmation."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_load_state("networkidle")
        
        # Enter mismatched passwords
        page.fill("#currentPassword", user_data["password"])
        page.fill("#newPassword", "new_password_123")
        page.fill("#confirmPassword", "different_password_456")
        page.click("#changePasswordBtn")
        
        # Should show error message about mismatch
        page.wait_for_selector('#passwordMessage[style*="display: block"].error', timeout=5000)
        error_message = page.locator("#passwordMessage.error")
        assert error_message.is_visible()
        assert "do not match" in error_message.inner_text().lower()
    
    def test_change_password_too_short(self, authenticated_page):
        """E2E: Try to change password to one that's too short."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_load_state("networkidle")
        
        # Try to set weak password
        page.fill("#currentPassword", user_data["password"])
        page.fill("#newPassword", "weak")
        page.fill("#confirmPassword", "weak")
        page.click("#changePasswordBtn")
        
        # Should show error message
        page.wait_for_selector('#passwordMessage[style*="display: block"].error', timeout=5000)
        error_message = page.locator("#passwordMessage.error")
        assert error_message.is_visible()


class TestCompleteProfileFlow:
    """Test complete end-to-end flows involving profile management."""
    
    def test_complete_flow_register_login_update_profile_change_password_relogin(self, page):
        """E2E: Complete flow from registration through profile updates to re-login."""
        # Step 1: Register new user
        timestamp = int(time.time() * 1000)
        username = f"complete_flow_{timestamp}"
        email = f"complete_flow_{timestamp}@example.com"
        password = "initial_password_123"
        
        page.goto("http://localhost:8000/static/register.html")
        page.fill("input[name='username']", username)
        page.fill("input[name='email']", email)
        page.fill("input[name='password']", password)
        page.fill("input[id='confirmPassword']", password)
        page.click("button[type='submit']")
        
        # Step 2: Login
        page.wait_for_url("**/login.html", timeout=5000)
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")
        page.wait_for_url("**/calculations.html", timeout=5000)
        
        # Step 3: Navigate to profile and update EMAIL ONLY (username change invalidates token)
        page.click('a.profile-btn')
        page.wait_for_url("**/profile.html", timeout=5000)
        page.wait_for_load_state("networkidle")
        
        new_email = f"updated_{email}"
        page.fill("#email", new_email)
        page.click("#updateProfileBtn")
        
        # Wait for success message to appear
        page.wait_for_function(
            "document.querySelector('#profileMessage').style.display === 'block' && document.querySelector('#profileMessage').classList.contains('success')",
            timeout=10000
        )
        
        # Step 4: Change password (still on profile page)
        new_password = "new_secure_password_789"
        page.wait_for_timeout(1000)  # Wait for form to reset
        page.fill("#currentPassword", password)
        page.fill("#newPassword", new_password)
        page.fill("#confirmPassword", new_password)
        page.click("#changePasswordBtn")
        
        # Wait for password success message
        page.wait_for_function(
            "document.querySelector('#passwordMessage').style.display === 'block' && document.querySelector('#passwordMessage').classList.contains('success')",
            timeout=10000
        )
        
        # Step 5: Logout
        page.click("#logoutBtn")
        page.wait_for_url("**/login.html", timeout=5000)
        
        # Step 6: Login with NEW credentials (original username and new password)
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", new_password)
        page.click("button[type='submit']")
        page.wait_for_url("**/calculations.html", timeout=5000)
        
        # Step 7: Verify we're successfully logged in
        assert "calculations.html" in page.url
        
        # Step 8: Navigate back to profile to verify all changes persisted
        page.click('a.profile-btn')
        page.wait_for_url("**/profile.html", timeout=5000)
        page.wait_for_load_state("networkidle")
        
        # Verify updated email is displayed (username unchanged)
        assert page.locator("#currentUsername").inner_text() == username
        assert page.locator("#currentEmail").inner_text() == new_email
    
    def test_old_credentials_fail_after_profile_update(self, page):
        """E2E: Verify old credentials don't work after profile update."""
        # Step 1: Register and login
        timestamp = int(time.time() * 1000)
        original_username = f"old_creds_{timestamp}"
        email = f"old_creds_{timestamp}@example.com"
        original_password = "original_password_123"
        
        page.goto("http://localhost:8000/static/register.html")
        page.fill("input[name='username']", original_username)
        page.fill("input[name='email']", email)
        page.fill("input[name='password']", original_password)
        page.fill("input[id='confirmPassword']", original_password)
        page.click("button[type='submit']")
        
        page.wait_for_url("**/login.html", timeout=5000)
        page.fill("input[name='username']", original_username)
        page.fill("input[name='password']", original_password)
        page.click("button[type='submit']")
        page.wait_for_url("**/calculations.html", timeout=5000)
        
        # Step 2: Update username and password
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_load_state("networkidle")
        
        new_username = f"{original_username}_new"
        new_password = "new_password_456"
        
        page.fill("#username", new_username)
        page.click("#updateProfileBtn")
        wait_for_profile_success(page)
        
        page.fill("#currentPassword", original_password)
        page.fill("#newPassword", new_password)
        page.fill("#confirmPassword", new_password)
        page.click("#changePasswordBtn")
        page.wait_for_selector("#passwordMessage.success", timeout=5000)
        
        # Step 3: Logout
        page.click("#logoutBtn")
        page.wait_for_url("**/login.html", timeout=5000)
        
        # Step 4: Try to login with OLD username and OLD password (should fail)
        page.fill("input[name='username']", original_username)
        page.fill("input[name='password']", original_password)
        page.click("button[type='submit']")
        
        # Should show error message (not redirect)
        page.wait_for_selector(".message.error", timeout=5000)
        error_message = page.locator(".message.error")
        assert error_message.is_visible()
        
        # Should still be on login page
        assert "login.html" in page.url


class TestNavigationAndUI:
    """Test navigation and UI interactions on profile page."""
    
    def test_navigation_to_dashboard(self, authenticated_page):
        """E2E: Test navigation from profile to dashboard."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        
        # Click Dashboard button
        page.click('a.btn-secondary:has-text("Dashboard")')
        
        # Should navigate to calculations page
        page.wait_for_url("**/calculations.html", timeout=5000)
        assert "calculations.html" in page.url
    
    def test_logout_from_profile_page(self, authenticated_page):
        """E2E: Test logout functionality from profile page."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        
        # Click Logout button
        page.click("#logoutBtn")
        
        # Should redirect to login page
        page.wait_for_url("**/login.html", timeout=5000)
        assert "login.html" in page.url
        
        # Try to access profile page again (should redirect to login)
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_url("**/login.html", timeout=5000)
        assert "login.html" in page.url
    
    def test_success_messages_auto_hide(self, authenticated_page):
        """E2E: Verify success messages auto-hide after 5 seconds."""
        page, user_data = authenticated_page
        
        # Navigate to profile page
        page.goto("http://localhost:8000/static/profile.html")
        page.wait_for_load_state("networkidle")
        
        # Update email to trigger success message
        new_email = f"autohide_{user_data['email']}"
        page.fill("#email", new_email)
        page.click("#updateProfileBtn")
        
        # Wait for success message to appear
        wait_for_profile_success(page)
        success_message = page.locator(".message.success")
        assert success_message.is_visible()
        
        # Wait for auto-hide (5 seconds + buffer)
        page.wait_for_timeout(6000)
        
        # Message should be hidden
        assert not success_message.is_visible()
