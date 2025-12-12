"""
Unit and Integration tests for Reports/Statistics feature
"""
import pytest
from sqlalchemy.orm import Session
from app.models import User, Calculation


class TestStatisticsUnit:
    """Unit tests for statistics endpoint"""

    def test_stats_with_no_calculations(self, authenticated_client):
        """Test statistics with zero calculations"""
        response = authenticated_client.get("/calculations/stats")
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_calculations"] == 0
        assert data["operations_breakdown"] == []
        assert data["average_operand1"] is None
        assert data["average_operand2"] is None
        assert data["most_used_operation"] is None
        assert data["recent_calculations"] == []

    def test_stats_with_single_calculation(self, authenticated_client):
        """Test statistics with one calculation"""
        # Create a calculation
        authenticated_client.post(
            "/calculations/",
            json={"operand1": 10, "operand2": 5, "operation": "add"}
        )
        
        response = authenticated_client.get("/calculations/stats")
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_calculations"] == 1
        assert len(data["operations_breakdown"]) == 1
        assert data["operations_breakdown"][0]["operation"] == "add"
        assert data["operations_breakdown"][0]["count"] == 1
        assert data["operations_breakdown"][0]["percentage"] == 100.0
        assert data["most_used_operation"] == "add"
        assert data["average_operand1"] == 10.0
        assert data["average_operand2"] == 5.0
        assert len(data["recent_calculations"]) == 1

    def test_stats_with_multiple_operations(self, authenticated_client):
        """Test statistics with multiple different operations"""
        calculations = [
            {"operand1": 10, "operand2": 5, "operation": "add"},
            {"operand1": 20, "operand2": 10, "operation": "subtract"},
            {"operand1": 5, "operand2": 3, "operation": "multiply"},
            {"operand1": 15, "operand2": 3, "operation": "divide"},
        ]
        
        for calc in calculations:
            authenticated_client.post("/calculations/", json=calc)
        
        response = authenticated_client.get("/calculations/stats")
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_calculations"] == 4
        assert len(data["operations_breakdown"]) == 4
        
        # Each operation should have 25% (1 out of 4)
        for breakdown in data["operations_breakdown"]:
            assert breakdown["count"] == 1
            assert breakdown["percentage"] == 25.0

    def test_stats_operations_breakdown_percentages(self, authenticated_client):
        """Test that operation percentages are calculated correctly"""
        # Create 3 add, 2 multiply, 1 divide (total 6)
        for _ in range(3):
            authenticated_client.post(
                "/calculations/",
                json={"operand1": 10, "operand2": 5, "operation": "add"}
            )
        for _ in range(2):
            authenticated_client.post(
                "/calculations/",
                json={"operand1": 5, "operand2": 3, "operation": "multiply"}
            )
        authenticated_client.post(
            "/calculations/",
            json={"operand1": 15, "operand2": 3, "operation": "divide"}
        )
        
        response = authenticated_client.get("/calculations/stats")
        data = response.json()
        
        assert data["total_calculations"] == 6
        
        # Find each operation's breakdown
        add_breakdown = next((b for b in data["operations_breakdown"] if b["operation"] == "add"), None)
        multiply_breakdown = next((b for b in data["operations_breakdown"] if b["operation"] == "multiply"), None)
        divide_breakdown = next((b for b in data["operations_breakdown"] if b["operation"] == "divide"), None)
        
        assert add_breakdown["count"] == 3
        assert add_breakdown["percentage"] == 50.0  # 3/6 = 50%
        
        assert multiply_breakdown["count"] == 2
        assert multiply_breakdown["percentage"] == 33.33  # 2/6 = 33.33%
        
        assert divide_breakdown["count"] == 1
        assert divide_breakdown["percentage"] == 16.67  # 1/6 = 16.67%

    def test_stats_most_used_operation(self, authenticated_client):
        """Test that most_used_operation is correctly identified"""
        # Create 5 add, 2 multiply, 1 subtract
        for _ in range(5):
            authenticated_client.post(
                "/calculations/",
                json={"operand1": 10, "operand2": 5, "operation": "add"}
            )
        for _ in range(2):
            authenticated_client.post(
                "/calculations/",
                json={"operand1": 5, "operand2": 3, "operation": "multiply"}
            )
        authenticated_client.post(
            "/calculations/",
            json={"operand1": 20, "operand2": 5, "operation": "subtract"}
        )
        
        response = authenticated_client.get("/calculations/stats")
        data = response.json()
        
        assert data["most_used_operation"] == "add"

    def test_stats_average_calculations(self, authenticated_client):
        """Test that averages are calculated correctly"""
        calculations = [
            {"operand1": 10, "operand2": 5, "operation": "add"},
            {"operand1": 20, "operand2": 10, "operation": "add"},
            {"operand1": 30, "operand2": 15, "operation": "add"},
        ]
        
        for calc in calculations:
            authenticated_client.post("/calculations/", json=calc)
        
        response = authenticated_client.get("/calculations/stats")
        data = response.json()
        
        # Average of (10, 20, 30) = 20
        assert data["average_operand1"] == 20.0
        # Average of (5, 10, 15) = 10
        assert data["average_operand2"] == 10.0

    def test_stats_recent_calculations_limit(self, authenticated_client):
        """Test that recent_calculations respects the limit parameter"""
        # Create 15 calculations
        for i in range(15):
            authenticated_client.post(
                "/calculations/",
                json={"operand1": i, "operand2": i+1, "operation": "add"}
            )
        
        # Default limit is 10
        response = authenticated_client.get("/calculations/stats")
        data = response.json()
        assert len(data["recent_calculations"]) == 10
        
        # Test custom limit
        response = authenticated_client.get("/calculations/stats?limit=5")
        data = response.json()
        assert len(data["recent_calculations"]) == 5

    def test_stats_recent_calculations_ordered_by_date(self, authenticated_client):
        """Test that recent calculations are ordered by date descending"""
        # Create calculations with different operands
        for i in range(5):
            authenticated_client.post(
                "/calculations/",
                json={"operand1": i, "operand2": i+1, "operation": "add"}
            )
        
        response = authenticated_client.get("/calculations/stats")
        data = response.json()
        
        recent = data["recent_calculations"]
        assert len(recent) == 5
        
        # Most recent should have highest operand1 value (created last)
        assert recent[0]["operand1"] == 4
        assert recent[-1]["operand1"] == 0

    def test_stats_with_advanced_operations(self, authenticated_client):
        """Test statistics includes advanced operations (power, modulus, sqrt)"""
        calculations = [
            {"operand1": 2, "operand2": 8, "operation": "power"},
            {"operand1": 17, "operand2": 5, "operation": "modulus"},
            {"operand1": 25, "operand2": 0, "operation": "sqrt"},
        ]
        
        for calc in calculations:
            authenticated_client.post("/calculations/", json=calc)
        
        response = authenticated_client.get("/calculations/stats")
        data = response.json()
        
        assert data["total_calculations"] == 3
        assert len(data["operations_breakdown"]) == 3
        
        operations = [b["operation"] for b in data["operations_breakdown"]]
        assert "power" in operations
        assert "modulus" in operations
        assert "sqrt" in operations

    def test_stats_unauthorized(self, client):
        """Test that unauthorized users cannot access stats"""
        response = client.get("/calculations/stats")
        assert response.status_code == 401

    def test_stats_with_decimal_operands(self, authenticated_client):
        """Test statistics with decimal operands"""
        calculations = [
            {"operand1": 10.5, "operand2": 5.25, "operation": "add"},
            {"operand1": 20.75, "operand2": 10.5, "operation": "subtract"},
        ]
        
        for calc in calculations:
            authenticated_client.post("/calculations/", json=calc)
        
        response = authenticated_client.get("/calculations/stats")
        data = response.json()
        
        # Average of (10.5, 20.75) = 15.625
        assert data["average_operand1"] == 15.62 or abs(data["average_operand1"] - 15.625) < 0.01
        # Average of (5.25, 10.5) = 7.875
        assert data["average_operand2"] == 7.88 or abs(data["average_operand2"] - 7.875) < 0.01


class TestStatisticsIntegration:
    """Integration tests for statistics endpoint"""

    def test_stats_user_isolation(self, client, db_session):
        """Test that users only see their own statistics"""
        from app.auth import get_password_hash
        
        # Create two users
        user1 = User(username="user1", email="user1@test.com", hashed_password=get_password_hash("password123"))
        user2 = User(username="user2", email="user2@test.com", hashed_password=get_password_hash("password123"))
        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()

        # Login as user1 and create calculations
        login1 = client.post("/users/login", json={"username": "user1", "password": "password123"})
        token1 = login1.json()["access_token"]
        
        for _ in range(3):
            client.post(
                "/calculations/",
                headers={"Authorization": f"Bearer {token1}"},
                json={"operand1": 10, "operand2": 5, "operation": "add"}
            )

        # Login as user2 and create calculations
        login2 = client.post("/users/login", json={"username": "user2", "password": "password123"})
        token2 = login2.json()["access_token"]
        
        for _ in range(5):
            client.post(
                "/calculations/",
                headers={"Authorization": f"Bearer {token2}"},
                json={"operand1": 20, "operand2": 10, "operation": "multiply"}
            )

        # User1 should only see their 3 calculations
        stats1 = client.get("/calculations/stats", headers={"Authorization": f"Bearer {token1}"})
        data1 = stats1.json()
        assert data1["total_calculations"] == 3
        assert data1["most_used_operation"] == "add"

        # User2 should only see their 5 calculations
        stats2 = client.get("/calculations/stats", headers={"Authorization": f"Bearer {token2}"})
        data2 = stats2.json()
        assert data2["total_calculations"] == 5
        assert data2["most_used_operation"] == "multiply"

    def test_stats_database_accuracy(self, authenticated_client, db_session, test_user):
        """Test that statistics match actual database records"""
        # Create specific calculations
        calculations = [
            {"operand1": 10, "operand2": 5, "operation": "add"},
            {"operand1": 20, "operand2": 10, "operation": "add"},
            {"operand1": 15, "operand2": 3, "operation": "divide"},
        ]
        
        for calc in calculations:
            authenticated_client.post("/calculations/", json=calc)
        
        # Get stats from API
        response = authenticated_client.get("/calculations/stats")
        data = response.json()
        
        # Verify against actual database records
        db_count = db_session.query(Calculation).count()
        assert data["total_calculations"] == db_count
        
        # Verify operation counts
        add_count = db_session.query(Calculation).filter(Calculation.operation == "add").count()
        add_breakdown = next((b for b in data["operations_breakdown"] if b["operation"] == "add"), None)
        assert add_breakdown["count"] == add_count

    def test_stats_with_mixed_operations(self, authenticated_client):
        """Test statistics with a realistic mix of all operations"""
        operations_data = {
            "add": 10,
            "subtract": 8,
            "multiply": 6,
            "divide": 4,
            "power": 3,
            "modulus": 2,
            "sqrt": 1
        }
        
        # Create calculations for each operation
        for operation, count in operations_data.items():
            for i in range(count):
                if operation == "sqrt":
                    calc = {"operand1": 25, "operand2": 0, "operation": operation}
                else:
                    calc = {"operand1": 10 + i, "operand2": 5 + i, "operation": operation}
                authenticated_client.post("/calculations/", json=calc)
        
        response = authenticated_client.get("/calculations/stats")
        data = response.json()
        
        total = sum(operations_data.values())
        assert data["total_calculations"] == total
        assert len(data["operations_breakdown"]) == 7
        assert data["most_used_operation"] == "add"
        
        # Verify each operation's count
        for breakdown in data["operations_breakdown"]:
            expected_count = operations_data[breakdown["operation"]]
            assert breakdown["count"] == expected_count
            expected_percentage = round((expected_count / total) * 100, 2)
            assert breakdown["percentage"] == expected_percentage

    def test_stats_after_calculation_deletion(self, authenticated_client):
        """Test that statistics update correctly after deleting calculations"""
        # Create some calculations
        calc_ids = []
        for i in range(5):
            response = authenticated_client.post(
                "/calculations/",
                json={"operand1": 10 + i, "operand2": 5 + i, "operation": "add"}
            )
            calc_ids.append(response.json()["id"])
        
        # Check initial stats
        stats_before = authenticated_client.get("/calculations/stats")
        assert stats_before.json()["total_calculations"] == 5
        
        # Delete 2 calculations
        for calc_id in calc_ids[:2]:
            authenticated_client.delete(f"/calculations/{calc_id}")
        
        # Check updated stats
        stats_after = authenticated_client.get("/calculations/stats")
        assert stats_after.json()["total_calculations"] == 3

    def test_stats_after_calculation_update(self, authenticated_client):
        """Test that statistics reflect calculation updates"""
        # Create add calculation
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 10, "operand2": 5, "operation": "add"}
        )
        calc_id = response.json()["id"]
        
        # Initial stats
        stats_before = authenticated_client.get("/calculations/stats")
        data_before = stats_before.json()
        assert data_before["most_used_operation"] == "add"
        
        # Update to multiply
        authenticated_client.put(
            f"/calculations/{calc_id}",
            json={"operand1": 10, "operand2": 5, "operation": "multiply"}
        )
        
        # Updated stats
        stats_after = authenticated_client.get("/calculations/stats")
        data_after = stats_after.json()
        assert data_after["most_used_operation"] == "multiply"
