"""
End-to-end tests for Reports/Statistics feature
Testing complete user workflows from login through viewing reports
"""
import pytest
from playwright.sync_api import Page, expect


class TestReportsPageE2E:
    """E2E tests for reports/statistics page"""

    def test_reports_page_accessible_when_authenticated(self, authenticated_page):
        """Test that authenticated users can access the reports page"""
        page = authenticated_page
        
        # Navigate to reports page
        page.goto("http://localhost:8000/static/reports.html")
        page.wait_for_load_state("networkidle")
        
        # Should see the reports page header
        expect(page.locator("h1")).to_contain_text("Reports & Statistics")
        
        # Should see stats content (even if empty)
        page.wait_for_selector("#statsContent", timeout=10000)

    def test_reports_page_redirects_when_unauthenticated(self, page):
        """Test that unauthenticated users are redirected to login"""
        # Clear any existing token
        page.goto("http://localhost:8000/static/login.html")
        page.evaluate("localStorage.removeItem('token')")
        
        # Try to access reports page
        page.goto("http://localhost:8000/static/reports.html")
        page.wait_for_load_state("networkidle")
        
        # Should be redirected to login page
        expect(page).to_have_url("http://localhost:8000/static/login.html")

    def test_reports_navigation_to_dashboard(self, authenticated_page):
        """Test navigation from reports to dashboard"""
        page = authenticated_page
        
        page.goto("http://localhost:8000/static/reports.html")
        page.wait_for_load_state("networkidle")
        
        # Click Dashboard button
        page.click("text=Dashboard")
        page.wait_for_load_state("networkidle")
        
        # Should be on calculations page
        expect(page).to_have_url("http://localhost:8000/static/calculations.html")

    def test_reports_navigation_to_profile(self, authenticated_page):
        """Test navigation from reports to profile"""
        page = authenticated_page
        
        page.goto("http://localhost:8000/static/reports.html")
        page.wait_for_load_state("networkidle")
        
        # Click Profile button
        page.click("text=Profile")
        page.wait_for_load_state("networkidle")
        
        # Should be on profile page
        expect(page).to_have_url("http://localhost:8000/static/profile.html")

    def test_reports_displays_zero_stats_for_new_user(self, authenticated_page):
        """Test that reports show zero statistics for users with no calculations"""
        page = authenticated_page
        
        page.goto("http://localhost:8000/static/reports.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("#statsContent", timeout=10000)
        
        # Check that total calculations is 0
        total_calc = page.locator("#totalCalculations").text_content()
        assert total_calc == "0"
        
        # Check that most used operation shows dash
        most_used = page.locator("#mostUsedOperation").text_content()
        assert most_used == "-"

    def test_reports_displays_stats_after_creating_calculations(self, authenticated_page):
        """Test that reports update after creating calculations"""
        page = authenticated_page
        
        # First, create some calculations
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")
        
        # Create 3 calculations
        for i in range(3):
            page.fill("#operand1", str(10 + i))
            page.select_option("#operation", "add")
            page.fill("#operand2", str(5 + i))
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
        
        # Now navigate to reports
        page.goto("http://localhost:8000/static/reports.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("#statsContent", timeout=10000)
        
        # Check that total calculations is 3
        page.wait_for_selector("#totalCalculations", timeout=5000)
        total_calc = page.locator("#totalCalculations").text_content()
        assert "3" in total_calc
        
        # Check that most used operation is ADD
        most_used = page.locator("#mostUsedOperation").text_content()
        assert "ADD" in most_used.upper()

    def test_reports_shows_operations_breakdown(self, authenticated_page):
        """Test that operations breakdown table is displayed"""
        page = authenticated_page
        
        # Create calculations with different operations
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")
        
        operations = ["add", "subtract", "multiply"]
        for op in operations:
            page.fill("#operand1", "10")
            page.select_option("#operation", op)
            page.fill("#operand2", "5")
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
        
        # Navigate to reports
        page.goto("http://localhost:8000/static/reports.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("#statsContent", timeout=10000)
        
        # Check that operations breakdown table exists
        page.wait_for_selector(".operations-table", timeout=5000)
        table = page.locator(".operations-table")
        expect(table).to_be_visible()
        
        # Check that table has rows for each operation
        table_content = table.text_content()
        assert "add" in table_content.lower()
        assert "subtract" in table_content.lower()
        assert "multiply" in table_content.lower()

    def test_reports_shows_recent_history(self, authenticated_page):
        """Test that recent calculations history is displayed"""
        page = authenticated_page
        
        # Create some calculations
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")
        
        for i in range(5):
            page.fill("#operand1", str(10 + i))
            page.select_option("#operation", "add")
            page.fill("#operand2", str(5 + i))
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
        
        # Navigate to reports
        page.goto("http://localhost:8000/static/reports.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("#statsContent", timeout=10000)
        
        # Check that history table exists
        page.wait_for_selector(".history-table", timeout=5000)
        history_table = page.locator(".history-table")
        expect(history_table).to_be_visible()
        
        # Check that there are rows in the table
        rows = history_table.locator("tbody tr")
        count = rows.count()
        assert count == 5

    def test_reports_calculates_averages_correctly(self, authenticated_page):
        """Test that average operands are calculated and displayed correctly"""
        page = authenticated_page
        
        # Create calculations with known values
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")
        
        # Create 3 calculations: (10,5), (20,10), (30,15)
        # Average operand1 should be 20, average operand2 should be 10
        values = [(10, 5), (20, 10), (30, 15)]
        for op1, op2 in values:
            page.fill("#operand1", str(op1))
            page.select_option("#operation", "add")
            page.fill("#operand2", str(op2))
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
        
        # Navigate to reports
        page.goto("http://localhost:8000/static/reports.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("#statsContent", timeout=10000)
        
        # Check averages
        page.wait_for_selector("#avgOperand1", timeout=5000)
        avg1 = page.locator("#avgOperand1").text_content()
        avg2 = page.locator("#avgOperand2").text_content()
        
        # Average of (10, 20, 30) = 20
        assert "20" in avg1
        # Average of (5, 10, 15) = 10
        assert "10" in avg2

    def test_reports_shows_advanced_operations_in_breakdown(self, authenticated_page):
        """Test that advanced operations appear in the breakdown"""
        page = authenticated_page
        
        # Create calculations with advanced operations
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")
        
        # Create power calculation
        page.fill("#operand1", "2")
        page.select_option("#operation", "power")
        page.fill("#operand2", "8")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(500)
        
        # Create sqrt calculation
        page.fill("#operand1", "25")
        page.select_option("#operation", "sqrt")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(500)
        
        # Navigate to reports
        page.goto("http://localhost:8000/static/reports.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("#statsContent", timeout=10000)
        
        # Check operations breakdown includes advanced operations
        page.wait_for_selector(".operations-table", timeout=5000)
        
        # Should see power and sqrt badges
        power_badge = page.locator(".op-power")
        expect(power_badge).to_be_visible()
        
        sqrt_badge = page.locator(".op-sqrt")
        expect(sqrt_badge).to_be_visible()

    def test_reports_logout_functionality(self, authenticated_page):
        """Test that logout button works from reports page"""
        page = authenticated_page
        
        page.goto("http://localhost:8000/static/reports.html")
        page.wait_for_load_state("networkidle")
        
        # Click logout button
        page.click("text=Logout")
        page.wait_for_load_state("networkidle")
        
        # Should be redirected to login page
        expect(page).to_have_url("http://localhost:8000/static/login.html")

    def test_reports_accessible_from_calculations_dashboard(self, authenticated_page):
        """Test that Reports button works from calculations dashboard"""
        page = authenticated_page
        
        # Should be on calculations page
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")
        
        # Click Reports button
        page.click("text=📊 Reports")
        page.wait_for_load_state("networkidle")
        
        # Should be on reports page
        expect(page).to_have_url("http://localhost:8000/static/reports.html")
        expect(page.locator("h1")).to_contain_text("Reports & Statistics")

    def test_reports_shows_percentage_bars(self, authenticated_page):
        """Test that percentage bars are displayed in operations breakdown"""
        page = authenticated_page
        
        # Create some calculations
        page.goto("http://localhost:8000/static/calculations.html")
        page.wait_for_load_state("networkidle")
        
        for _ in range(3):
            page.fill("#operand1", "10")
            page.select_option("#operation", "add")
            page.fill("#operand2", "5")
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
        
        # Navigate to reports
        page.goto("http://localhost:8000/static/reports.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("#statsContent", timeout=10000)
        
        # Check for progress bars
        page.wait_for_selector(".progress-bar", timeout=5000)
        progress_bars = page.locator(".progress-bar")
        assert progress_bars.count() > 0

    def test_complete_reports_workflow(self, page):
        """Test complete workflow: register → login → create calculations → view reports"""
        # Register new user
        page.goto("http://localhost:8000/static/register.html")
        import time
        username = f"reportuser_{int(time.time())}"
        email = f"{username}@test.com"
        
        page.fill("#username", username)
        page.fill("#email", email)
        page.fill("#password", "testpass123")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")
        
        # Login
        page.goto("http://localhost:8000/static/login.html")
        page.fill("#username", username)
        page.fill("#password", "testpass123")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")
        
        # Should be on calculations page
        expect(page).to_have_url("http://localhost:8000/static/calculations.html")
        
        # Create various calculations
        calc_data = [
            ("10", "add", "5"),
            ("20", "subtract", "8"),
            ("5", "multiply", "4"),
            ("2", "power", "3"),
        ]
        
        for op1, operation, op2 in calc_data:
            page.fill("#operand1", op1)
            page.select_option("#operation", operation)
            page.fill("#operand2", op2)
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
        
        # Navigate to reports
        page.click("text=📊 Reports")
        page.wait_for_load_state("networkidle")
        
        # Verify we're on reports page
        expect(page).to_have_url("http://localhost:8000/static/reports.html")
        
        # Verify stats are displayed
        page.wait_for_selector("#statsContent", timeout=10000)
        total = page.locator("#totalCalculations").text_content()
        assert "4" in total
        
        # Verify operations breakdown exists
        page.wait_for_selector(".operations-table", timeout=5000)
        
        # Verify recent history exists
        page.wait_for_selector(".history-table", timeout=5000)
        rows = page.locator(".history-table tbody tr")
        assert rows.count() == 4
