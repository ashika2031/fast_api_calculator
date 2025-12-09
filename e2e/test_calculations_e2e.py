"""
E2E tests for Calculations BREAD operations using Playwright.
Tests cover positive and negative scenarios for Browse, Read, Edit, Add, Delete.
"""
import pytest
from playwright.sync_api import Page, expect
import time


@pytest.fixture
def authenticated_page(page: Page, base_url):
    """Fixture that logs in a user and returns the page with auth token."""
    # Register a new user
    timestamp = int(time.time() * 1000)
    username = f"calc_user_{timestamp}"
    unique_email = f"{username}@test.com"
    
    page.goto(f"{base_url}/static/register.html")
    page.fill('input[id="username"]', username)
    page.fill('input[id="email"]', unique_email)
    page.fill('input[id="password"]', "testpass123")
    page.fill('input[id="confirmPassword"]', "testpass123")
    page.click('button[type="submit"]')
    
    # Wait for redirect to login
    page.wait_for_url("**/login.html", timeout=5000)
    
    # Login with the same username
    page.fill('input[id="username"]', username)
    page.fill('input[id="password"]', "testpass123")
    page.click('button[type="submit"]')
    
    # Wait for redirect to calculations
    page.wait_for_url("**/calculations.html", timeout=5000)
    
    return page


class TestCalculationsAdd:
    """Test the ADD operation (Create new calculation)."""
    
    def test_add_calculation_addition(self, authenticated_page: Page):
        """Test adding a simple addition calculation."""
        page = authenticated_page
        
        # Fill in calculation form
        page.fill('input[id="operand1"]', '10')
        page.select_option('select[id="operation"]', 'add')
        page.fill('input[id="operand2"]', '5')
        
        # Submit form
        page.click('button[type="submit"]:has-text("Calculate")')
        
        # Wait for success message
        success_msg = page.locator('.message.success')
        expect(success_msg).to_be_visible(timeout=5000)
        expect(success_msg).to_contain_text('Result: 15')
        
        # Verify calculation appears in table
        table = page.locator('table tbody')
        expect(table).to_contain_text('10')
        expect(table).to_contain_text('5')
        expect(table).to_contain_text('15')
    
    def test_add_calculation_all_operations(self, authenticated_page: Page):
        """Test all four operations: add, subtract, multiply, divide."""
        page = authenticated_page
        
        operations = [
            ('add', 10, 5, 15),
            ('subtract', 20, 8, 12),
            ('multiply', 6, 7, 42),
            ('divide', 100, 4, 25)
        ]
        
        for operation, op1, op2, expected_result in operations:
            page.fill('input[id="operand1"]', str(op1))
            page.select_option('select[id="operation"]', operation)
            page.fill('input[id="operand2"]', str(op2))
            page.click('button[type="submit"]:has-text("Calculate")')
            
            # Wait for success message
            success_msg = page.locator('.message.success')
            expect(success_msg).to_be_visible(timeout=5000)
            expect(success_msg).to_contain_text(f'Result: {expected_result}')
            
            # Small delay between operations
            time.sleep(0.5)
    
    def test_add_calculation_division_by_zero(self, authenticated_page: Page):
        """Test that division by zero shows error."""
        page = authenticated_page
        
        page.fill('input[id="operand1"]', '10')
        page.select_option('select[id="operation"]', 'divide')
        page.fill('input[id="operand2"]', '0')
        page.click('button[type="submit"]:has-text("Calculate")')
        
        # Wait for error message
        error_msg = page.locator('.message.error')
        expect(error_msg).to_be_visible(timeout=5000)
        expect(error_msg).to_contain_text('Division by zero')
    
    def test_add_calculation_decimal_numbers(self, authenticated_page: Page):
        """Test calculations with decimal numbers."""
        page = authenticated_page
        
        page.fill('input[id="operand1"]', '3.14')
        page.select_option('select[id="operation"]', 'multiply')
        page.fill('input[id="operand2"]', '2')
        page.click('button[type="submit"]:has-text("Calculate")')
        
        success_msg = page.locator('.message.success')
        expect(success_msg).to_be_visible(timeout=5000)
        expect(success_msg).to_contain_text('Result: 6.28')


class TestCalculationsBrowse:
    """Test the BROWSE operation (List all calculations)."""
    
    def test_browse_empty_calculations(self, authenticated_page: Page):
        """Test browsing when no calculations exist."""
        page = authenticated_page
        
        # Check for empty state message
        no_data = page.locator('.no-data')
        # Note: might show "Loading" briefly, so wait for the actual message
        page.wait_for_timeout(1000)
        # After loading, should show "No calculations yet"
        expect(page.locator('text=No calculations yet')).to_be_visible(timeout=5000)
    
    def test_browse_with_calculations(self, authenticated_page: Page):
        """Test browsing displays calculations correctly."""
        page = authenticated_page
        
        # Add a calculation first
        page.fill('input[id="operand1"]', '100')
        page.select_option('select[id="operation"]', 'add')
        page.fill('input[id="operand2"]', '50')
        page.click('button[type="submit"]:has-text("Calculate")')
        
        # Wait for success
        page.wait_for_selector('.message.success', timeout=5000)
        
        # Verify table appears and contains data
        table = page.locator('table')
        expect(table).to_be_visible()
        
        # Check table headers
        expect(page.locator('thead')).to_contain_text('ID')
        expect(page.locator('thead')).to_contain_text('Operation')
        expect(page.locator('thead')).to_contain_text('Result')
        expect(page.locator('thead')).to_contain_text('Actions')
        
        # Check calculation data
        tbody = page.locator('tbody')
        expect(tbody).to_contain_text('100')
        expect(tbody).to_contain_text('50')
        expect(tbody).to_contain_text('150')


class TestCalculationsRead:
    """Test the READ operation (View specific calculation details)."""
    
    def test_read_calculation_via_edit(self, authenticated_page: Page):
        """Test reading a calculation by clicking Edit button."""
        page = authenticated_page
        
        # Add a calculation
        page.fill('input[id="operand1"]', '25')
        page.select_option('select[id="operation"]', 'multiply')
        page.fill('input[id="operand2"]', '4')
        page.click('button[type="submit"]:has-text("Calculate")')
        page.wait_for_selector('.message.success', timeout=5000)
        
        # Click Edit button
        edit_btn = page.locator('button.btn-edit').first
        edit_btn.click()
        
        # Verify edit form is populated with correct data
        expect(page.locator('#editOperand1')).to_have_value('25')
        expect(page.locator('#editOperation')).to_have_value('multiply')
        expect(page.locator('#editOperand2')).to_have_value('4')
        
        # Verify edit section is visible
        expect(page.locator('#editSection')).to_be_visible()
        expect(page.locator('#addSection')).not_to_be_visible()


class TestCalculationsEdit:
    """Test the EDIT operation (Update existing calculation)."""
    
    def test_edit_calculation_success(self, authenticated_page: Page):
        """Test successfully editing a calculation."""
        page = authenticated_page
        
        # Add a calculation
        page.fill('input[id="operand1"]', '10')
        page.select_option('select[id="operation"]', 'add')
        page.fill('input[id="operand2"]', '5')
        page.click('button[type="submit"]:has-text("Calculate")')
        page.wait_for_selector('.message.success', timeout=5000)
        
        # Click Edit
        page.locator('button.btn-edit').first.click()
        
        # Modify the calculation
        page.fill('input[id="editOperand1"]', '20')
        page.select_option('select[id="editOperation"]', 'multiply')
        page.fill('input[id="editOperand2"]', '3')
        
        # Submit update
        page.click('button[type="submit"]:has-text("Update")')
        
        # Wait for success message
        success_msg = page.locator('.message.success')
        expect(success_msg).to_be_visible(timeout=5000)
        expect(success_msg).to_contain_text('updated')
        expect(success_msg).to_contain_text('60')  # 20 * 3
        
        # Verify table updated
        tbody = page.locator('tbody')
        expect(tbody).to_contain_text('20')
        expect(tbody).to_contain_text('3')
        expect(tbody).to_contain_text('60')
    
    def test_edit_calculation_cancel(self, authenticated_page: Page):
        """Test canceling an edit operation."""
        page = authenticated_page
        
        # Add a calculation
        page.fill('input[id="operand1"]', '7')
        page.select_option('select[id="operation"]', 'add')
        page.fill('input[id="operand2"]', '3')
        page.click('button[type="submit"]:has-text("Calculate")')
        page.wait_for_selector('.message.success', timeout=5000)
        
        # Click Edit
        page.locator('button.btn-edit').first.click()
        expect(page.locator('#editSection')).to_be_visible()
        
        # Click Cancel
        page.click('button:has-text("Cancel")')
        
        # Verify back to add form
        expect(page.locator('#addSection')).to_be_visible()
        expect(page.locator('#editSection')).not_to_be_visible()
    
    def test_edit_calculation_division_by_zero(self, authenticated_page: Page):
        """Test editing with invalid data (division by zero)."""
        page = authenticated_page
        
        # Add a calculation
        page.fill('input[id="operand1"]', '10')
        page.select_option('select[id="operation"]', 'add')
        page.fill('input[id="operand2"]', '5')
        page.click('button[type="submit"]:has-text("Calculate")')
        page.wait_for_selector('.message.success', timeout=5000)
        
        # Edit to division by zero
        page.locator('button.btn-edit').first.click()
        page.select_option('select[id="editOperation"]', 'divide')
        page.fill('input[id="editOperand2"]', '0')
        page.click('button[type="submit"]:has-text("Update")')
        
        # Should show error
        error_msg = page.locator('.message.error')
        expect(error_msg).to_be_visible(timeout=5000)
        expect(error_msg).to_contain_text('Division by zero')


class TestCalculationsDelete:
    """Test the DELETE operation (Remove calculation)."""
    
    def test_delete_calculation_success(self, authenticated_page: Page):
        """Test successfully deleting a calculation."""
        page = authenticated_page
        
        # Add a calculation
        page.fill('input[id="operand1"]', '99')
        page.select_option('select[id="operation"]', 'subtract')
        page.fill('input[id="operand2"]', '9')
        page.click('button[type="submit"]:has-text("Calculate")')
        page.wait_for_selector('.message.success', timeout=5000)
        
        # Verify calculation exists
        expect(page.locator('tbody')).to_contain_text('99')
        
        # Click Delete (handle confirm dialog)
        page.once("dialog", lambda dialog: dialog.accept())
        page.locator('button.btn-delete').first.click()
        
        # Wait for success message
        success_msg = page.locator('.message.success')
        expect(success_msg).to_be_visible(timeout=5000)
        expect(success_msg).to_contain_text('deleted')
        
        # Verify calculation removed from table
        page.wait_for_timeout(1000)
        # Should show empty state
        expect(page.locator('text=No calculations yet')).to_be_visible(timeout=5000)
    
    def test_delete_calculation_cancel(self, authenticated_page: Page):
        """Test canceling a delete operation."""
        page = authenticated_page
        
        # Add a calculation
        page.fill('input[id="operand1"]', '50')
        page.select_option('select[id="operation"]', 'divide')
        page.fill('input[id="operand2"]', '2')
        page.click('button[type="submit"]:has-text("Calculate")')
        page.wait_for_selector('.message.success', timeout=5000)
        
        # Click Delete but cancel
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.locator('button.btn-delete').first.click()
        
        # Calculation should still be there
        page.wait_for_timeout(500)
        expect(page.locator('tbody')).to_contain_text('50')
        expect(page.locator('tbody')).to_contain_text('25')
    
    def test_delete_multiple_calculations(self, authenticated_page: Page):
        """Test deleting multiple calculations."""
        page = authenticated_page
        
        # Add 3 calculations
        calculations = [
            ('10', 'add', '5'),
            ('20', 'multiply', '2'),
            ('100', 'divide', '4')
        ]
        
        for op1, operation, op2 in calculations:
            page.fill('input[id="operand1"]', op1)
            page.select_option('select[id="operation"]', operation)
            page.fill('input[id="operand2"]', op2)
            page.click('button[type="submit"]:has-text("Calculate")')
            page.wait_for_selector('.message.success', timeout=5000)
            time.sleep(0.5)
        
        # Verify 3 rows exist
        rows = page.locator('tbody tr')
        expect(rows).to_have_count(3)
        
        # Delete first calculation
        page.once("dialog", lambda dialog: dialog.accept())
        page.locator('button.btn-delete').first.click()
        page.wait_for_selector('.message.success', timeout=5000)
        page.wait_for_timeout(1000)
        
        # Should have 2 rows now
        rows = page.locator('tbody tr')
        expect(rows).to_have_count(2)


class TestCalculationsNegativeScenarios:
    """Test negative scenarios and error handling."""
    
    def test_unauthorized_access_redirects_to_login(self, page: Page, base_url):
        """Test that accessing calculations without login redirects to login page."""
        # Clear localStorage to ensure no token
        page.goto(f"{base_url}/static/calculations.html")
        page.evaluate("localStorage.clear()")
        page.reload()
        
        # Should redirect to login
        page.wait_for_url("**/login.html", timeout=5000)
    
    def test_add_with_empty_fields(self, authenticated_page: Page):
        """Test form validation prevents submission with empty fields."""
        page = authenticated_page
        
        # Try to submit empty form
        page.click('button[type="submit"]:has-text("Calculate")')
        
        # Form should not submit (HTML5 validation)
        # Success message should not appear
        success_msg = page.locator('.message.success')
        expect(success_msg).not_to_be_visible()
    
    def test_logout_functionality(self, authenticated_page: Page, base_url):
        """Test that logout clears token and redirects to login."""
        page = authenticated_page
        
        # Click logout
        page.click('button.logout-btn')
        
        # Should redirect to login
        page.wait_for_url("**/login.html", timeout=5000)
        
        # Try to access calculations again - should redirect to login
        page.goto(f"{base_url}/static/calculations.html")
        page.wait_for_url("**/login.html", timeout=5000)
