"""
End-to-end tests for advanced calculation operations (power, modulus, sqrt)
Testing complete user workflows from login through calculation operations
"""
import pytest
from playwright.sync_api import Page, expect


class TestAdvancedCalculationsE2E:
    """E2E tests for advanced calculation operations"""

    def test_power_calculation_via_ui(self, authenticated_page):
        """Test creating a power calculation through the UI: 2^8 = 256"""
        page = authenticated_page

        # Navigate to calculations page
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")

        # Fill in power calculation: 2^8
        page.fill("#operand1", "2")
        page.select_option("#operation", "power")
        page.fill("#operand2", "8")

        # Submit the form
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Wait for success message
        page.wait_for_selector(".message.success", timeout=10000)
        success_message = page.locator(".message.success").text_content()
        assert "256" in success_message
        assert "successful" in success_message.lower()

        # Verify the calculation appears in the table
        page.wait_for_selector("table tbody tr", timeout=5000)
        table_content = page.locator("table").text_content()
        assert "power" in table_content
        assert "256" in table_content

    def test_modulus_calculation_via_ui(self, authenticated_page):
        """Test creating a modulus calculation through the UI: 17 % 5 = 2"""
        page = authenticated_page

        # Navigate to calculations page
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")

        # Fill in modulus calculation: 17 % 5
        page.fill("#operand1", "17")
        page.select_option("#operation", "modulus")
        page.fill("#operand2", "5")

        # Submit the form
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Wait for success message
        page.wait_for_selector(".message.success", timeout=10000)
        success_message = page.locator(".message.success").text_content()
        assert "2" in success_message
        assert "successful" in success_message.lower()

        # Verify the calculation appears in the table
        page.wait_for_selector("table tbody tr", timeout=5000)
        table_content = page.locator("table").text_content()
        assert "modulus" in table_content
        assert "2" in table_content

    def test_sqrt_calculation_via_ui(self, authenticated_page):
        """Test creating a sqrt calculation through the UI: √25 = 5"""
        page = authenticated_page

        # Navigate to calculations page
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")

        # Fill in sqrt calculation: √25
        page.fill("#operand1", "25")
        page.select_option("#operation", "sqrt")

        # Verify operand2 field is disabled for sqrt
        operand2_field = page.locator("#operand2")
        assert operand2_field.is_disabled()
        
        # Submit the form (operand2 should be auto-filled with 0)
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Wait for success message
        page.wait_for_selector(".message.success", timeout=10000)
        success_message = page.locator(".message.success").text_content()
        assert "5" in success_message
        assert "successful" in success_message.lower()

        # Verify the calculation appears in the table with sqrt formatting
        page.wait_for_selector("table tbody tr", timeout=5000)
        table_content = page.locator("table").text_content()
        assert "sqrt" in table_content
        assert "5" in table_content

    def test_sqrt_operand2_field_behavior(self, authenticated_page):
        """Test that operand2 field is disabled when sqrt is selected"""
        page = authenticated_page

        # Navigate to calculations page
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")

        # Initially select a regular operation (operand2 should be enabled)
        page.select_option("#operation", "add")
        operand2_field = page.locator("#operand2")
        assert not operand2_field.is_disabled()

        # Switch to sqrt (operand2 should become disabled)
        page.select_option("#operation", "sqrt")
        page.wait_for_timeout(200)  # Wait for change handler
        assert operand2_field.is_disabled()
        
        # Check that the field shows it's not needed
        placeholder = operand2_field.get_attribute("placeholder")
        assert "Not needed" in placeholder or placeholder == "Not needed for √"

        # Switch back to add (operand2 should be enabled again)
        page.select_option("#operation", "add")
        page.wait_for_timeout(200)  # Wait for change handler
        assert not operand2_field.is_disabled()

    def test_power_overflow_shows_error(self, authenticated_page):
        """Test that power overflow shows proper error message"""
        page = authenticated_page

        # Navigate to calculations page
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")

        # Try to calculate a huge power that will overflow: 999^999
        page.fill("#operand1", "999")
        page.select_option("#operation", "power")
        page.fill("#operand2", "999")

        # Submit the form
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Wait for error message
        page.wait_for_selector(".message.error", timeout=10000)
        error_message = page.locator(".message.error").text_content()
        assert "error" in error_message.lower()
        assert "Power calculation error" in error_message or "error" in error_message.lower()

    def test_modulus_by_zero_shows_error(self, authenticated_page):
        """Test that modulus by zero shows proper error message"""
        page = authenticated_page

        # Navigate to calculations page
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")

        # Try to calculate modulus by zero: 10 % 0
        page.fill("#operand1", "10")
        page.select_option("#operation", "modulus")
        page.fill("#operand2", "0")

        # Submit the form
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Wait for error message
        page.wait_for_selector(".message.error", timeout=10000)
        error_message = page.locator(".message.error").text_content()
        assert "error" in error_message.lower()
        assert ("Modulus by zero" in error_message or 
                "zero" in error_message.lower() or 
                "not allowed" in error_message.lower())

    def test_sqrt_negative_shows_error(self, authenticated_page):
        """Test that sqrt of negative number shows proper error message"""
        page = authenticated_page

        # Navigate to calculations page
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")

        # Try to calculate sqrt of negative: √(-1)
        page.fill("#operand1", "-1")
        page.select_option("#operation", "sqrt")

        # Submit the form
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Wait for error message
        page.wait_for_selector(".message.error", timeout=10000)
        error_message = page.locator(".message.error").text_content()
        assert "error" in error_message.lower()
        assert ("negative" in error_message.lower() or 
                "not allowed" in error_message.lower())

    def test_edit_calculation_with_advanced_operation(self, authenticated_page):
        """Test editing a calculation to change it to an advanced operation"""
        page = authenticated_page

        # Navigate to calculations page and create a basic calculation
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")

        # Create initial calculation: 10 + 5
        page.fill("#operand1", "10")
        page.select_option("#operation", "add")
        page.fill("#operand2", "5")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Wait for calculation to appear and click edit
        page.wait_for_selector(".btn-edit", timeout=5000)
        page.click(".btn-edit:last-of-type")
        
        # Wait for edit form to appear
        page.wait_for_selector("#editSection", timeout=5000)
        expect(page.locator("#editSection")).to_be_visible()

        # Change to power operation: 2^10 = 1024
        page.fill("#editOperand1", "2")
        page.select_option("#editOperation", "power")
        page.fill("#editOperand2", "10")

        # Submit the update
        page.click("#editSection button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Wait for success message
        page.wait_for_selector(".message.success", timeout=10000)
        success_message = page.locator(".message.success").text_content()
        assert "1024" in success_message or "updated" in success_message.lower()

        # Verify the updated calculation in the table
        page.wait_for_selector("table tbody tr", timeout=5000)
        table_content = page.locator("table").text_content()
        assert "power" in table_content
        assert "1024" in table_content

    def test_browse_shows_advanced_operations_correctly(self, authenticated_page):
        """Test that all advanced operations display correctly in the browse table"""
        page = authenticated_page

        # Navigate to calculations page
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")

        # Create one of each advanced operation
        operations = [
            {"operand1": "3", "operand2": "4", "operation": "power", "result": "81"},
            {"operand1": "15", "operand2": "4", "operation": "modulus", "result": "3"},
            {"operand1": "36", "operand2": "0", "operation": "sqrt", "result": "6"}
        ]

        for op in operations:
            page.fill("#operand1", op["operand1"])
            page.select_option("#operation", op["operation"])
            
            # Handle sqrt special case
            if op["operation"] != "sqrt":
                page.fill("#operand2", op["operand2"])
                
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")
            page.wait_for_selector(".message.success", timeout=10000)

        # Verify all operations appear in table with correct badges
        page.wait_for_selector("table tbody tr", timeout=5000)
        
        # Check for operation badges
        power_badge = page.locator(".op-power")
        expect(power_badge).to_be_visible()
        
        modulus_badge = page.locator(".op-modulus")
        expect(modulus_badge).to_be_visible()
        
        sqrt_badge = page.locator(".op-sqrt")
        expect(sqrt_badge).to_be_visible()

        # Verify results are displayed
        table_content = page.locator("table").text_content()
        assert "81" in table_content
        assert "3" in table_content
        assert "6" in table_content

    def test_edit_sqrt_calculation_operand2_disabled(self, authenticated_page):
        """Test that when editing a sqrt calculation, operand2 field is disabled"""
        page = authenticated_page

        # Navigate and create a sqrt calculation
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")

        # Create sqrt calculation
        page.fill("#operand1", "49")
        page.select_option("#operation", "sqrt")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Click edit on the sqrt calculation
        page.wait_for_selector(".btn-edit", timeout=5000)
        page.click(".btn-edit:last-of-type")
        
        # Wait for edit form
        page.wait_for_selector("#editSection", timeout=5000)
        
        # Verify operand2 field is disabled since operation is sqrt
        edit_operand2 = page.locator("#editOperand2")
        page.wait_for_timeout(500)  # Wait for handleEditOperationChange to run
        assert edit_operand2.is_disabled()

    def test_complete_advanced_calculations_workflow(self, page):
        """Test complete workflow: register → login → create all advanced operations → edit → delete"""
        # Register new user
        page.goto("http://localhost:8000/static/register.html")
        page.fill("#username", "advanceduser")
        page.fill("#email", "advanced@test.com")
        page.fill("#password", "testpass123")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Login
        page.goto("http://localhost:8000/static/login.html")
        page.fill("#username", "advanceduser")
        page.fill("#password", "testpass123")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Should be redirected to calculations page
        expect(page).to_have_url("http://localhost:8000/static/calculations.html")

        # Create power calculation
        page.fill("#operand1", "5")
        page.select_option("#operation", "power")
        page.fill("#operand2", "3")
        page.click("button[type='submit']")
        page.wait_for_selector(".message.success", timeout=10000)

        # Create modulus calculation
        page.fill("#operand1", "20")
        page.select_option("#operation", "modulus")
        page.fill("#operand2", "6")
        page.click("button[type='submit']")
        page.wait_for_selector(".message.success", timeout=10000)

        # Create sqrt calculation
        page.fill("#operand1", "100")
        page.select_option("#operation", "sqrt")
        page.click("button[type='submit']")
        page.wait_for_selector(".message.success", timeout=10000)

        # Verify all three calculations appear
        page.wait_for_selector("table tbody tr", timeout=5000)
        rows = page.locator("table tbody tr").count()
        assert rows >= 3

        # Edit the power calculation to modulus
        page.click(".btn-edit:first-of-type")
        page.wait_for_selector("#editSection", timeout=5000)
        page.select_option("#editOperation", "modulus")
        page.fill("#editOperand2", "2")
        page.click("#editSection button[type='submit']")
        page.wait_for_selector(".message.success", timeout=10000)

        # Delete one calculation
        page.click(".btn-delete:first-of-type")
        page.once("dialog", lambda dialog: dialog.accept())
        page.wait_for_load_state("networkidle")

        # Verify deletion
        page.wait_for_timeout(1000)
        new_row_count = page.locator("table tbody tr").count()
        assert new_row_count < rows

    def test_all_operations_displayed_in_dropdown(self, authenticated_page):
        """Test that all 7 operations are available in both add and edit form dropdowns"""
        page = authenticated_page

        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")

        # Check add form dropdown has all 7 operations
        add_operation_select = page.locator("#operation")
        add_options = add_operation_select.locator("option").all_text_contents()
        
        expected_operations = ["Add (+)", "Subtract (-)", "Multiply (×)", "Divide (÷)", 
                               "Power (^)", "Modulus (%)", "Square Root (√)"]
        
        for expected in expected_operations:
            assert any(expected in option for option in add_options), \
                f"'{expected}' not found in add form dropdown"

        # Create a calculation to access edit form
        page.fill("#operand1", "10")
        page.select_option("#operation", "add")
        page.fill("#operand2", "5")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Click edit to show edit form
        page.wait_for_selector(".btn-edit", timeout=5000)
        page.click(".btn-edit:last-of-type")
        page.wait_for_selector("#editSection", timeout=5000)

        # Check edit form dropdown has all 7 operations
        edit_operation_select = page.locator("#editOperation")
        edit_options = edit_operation_select.locator("option").all_text_contents()
        
        for expected in expected_operations:
            assert any(expected in option for option in edit_options), \
                f"'{expected}' not found in edit form dropdown"
