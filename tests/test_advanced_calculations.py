"""
Unit and Integration tests for advanced calculation operations (power, modulus, sqrt)
"""
import pytest
from sqlalchemy.orm import Session
from app.models import User, Calculation


class TestPowerOperationUnit:
    """Unit tests for power (exponentiation) operation"""

    def test_power_positive_exponent(self, authenticated_client):
        """Test power with positive exponent: 2^3 = 8"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 2, "operand2": 3, "operation": "power"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 8
        assert data["operation"] == "power"

    def test_power_negative_exponent(self, authenticated_client):
        """Test power with negative exponent: 2^-2 = 0.25"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 2, "operand2": -2, "operation": "power"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 0.25
        assert data["operation"] == "power"

    def test_power_decimal_exponent(self, authenticated_client):
        """Test power with decimal exponent: 4^0.5 = 2.0 (square root)"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 4, "operand2": 0.5, "operation": "power"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 2.0
        assert data["operation"] == "power"

    def test_power_zero_exponent(self, authenticated_client):
        """Test power with zero exponent: 5^0 = 1"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 5, "operand2": 0, "operation": "power"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 1
        assert data["operation"] == "power"

    def test_power_large_result(self, authenticated_client):
        """Test power with large result: 10^6 = 1000000"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 10, "operand2": 6, "operation": "power"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 1000000
        assert data["operation"] == "power"

    def test_power_very_large_exponent_overflow(self, authenticated_client):
        """Test power with overflow: very large exponent should raise error"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 999, "operand2": 999, "operation": "power"}
        )
        assert response.status_code == 400
        assert "Power calculation error" in response.json()["detail"]


class TestModulusOperationUnit:
    """Unit tests for modulus (%) operation"""

    def test_modulus_positive_operands(self, authenticated_client):
        """Test modulus with positive operands: 10 % 3 = 1"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 10, "operand2": 3, "operation": "modulus"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 1
        assert data["operation"] == "modulus"

    def test_modulus_negative_dividend(self, authenticated_client):
        """Test modulus with negative dividend: -10 % 3 = 2 (Python behavior)"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": -10, "operand2": 3, "operation": "modulus"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 2
        assert data["operation"] == "modulus"

    def test_modulus_negative_divisor(self, authenticated_client):
        """Test modulus with negative divisor: 10 % -3 = -2 (Python behavior)"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 10, "operand2": -3, "operation": "modulus"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == -2
        assert data["operation"] == "modulus"

    def test_modulus_decimal_operands(self, authenticated_client):
        """Test modulus with decimal operands: 10.5 % 3.2"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 10.5, "operand2": 3.2, "operation": "modulus"}
        )
        assert response.status_code == 201
        data = response.json()
        # 10.5 % 3.2 = 0.9 (approximately)
        assert abs(data["result"] - 0.9) < 0.01
        assert data["operation"] == "modulus"

    def test_modulus_by_zero(self, authenticated_client):
        """Test modulus by zero: should raise error"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 10, "operand2": 0, "operation": "modulus"}
        )
        assert response.status_code == 400
        assert "Modulus by zero is not allowed" in response.json()["detail"]

    def test_modulus_zero_dividend(self, authenticated_client):
        """Test modulus with zero dividend: 0 % 5 = 0"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 0, "operand2": 5, "operation": "modulus"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 0
        assert data["operation"] == "modulus"


class TestSqrtOperationUnit:
    """Unit tests for sqrt (square root) operation"""

    def test_sqrt_perfect_square(self, authenticated_client):
        """Test sqrt of perfect square: sqrt(16) = 4.0"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 16, "operand2": 0, "operation": "sqrt"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 4.0
        assert data["operation"] == "sqrt"

    def test_sqrt_non_perfect_square(self, authenticated_client):
        """Test sqrt of non-perfect square: sqrt(2) ≈ 1.414"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 2, "operand2": 0, "operation": "sqrt"}
        )
        assert response.status_code == 201
        data = response.json()
        assert abs(data["result"] - 1.414213562373095) < 0.0001
        assert data["operation"] == "sqrt"

    def test_sqrt_of_zero(self, authenticated_client):
        """Test sqrt of zero: sqrt(0) = 0"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 0, "operand2": 0, "operation": "sqrt"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 0
        assert data["operation"] == "sqrt"

    def test_sqrt_of_one(self, authenticated_client):
        """Test sqrt of one: sqrt(1) = 1"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 1, "operand2": 0, "operation": "sqrt"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 1
        assert data["operation"] == "sqrt"

    def test_sqrt_large_number(self, authenticated_client):
        """Test sqrt of large number: sqrt(10000) = 100"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 10000, "operand2": 0, "operation": "sqrt"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 100
        assert data["operation"] == "sqrt"

    def test_sqrt_of_negative(self, authenticated_client):
        """Test sqrt of negative number: should raise error"""
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": -1, "operand2": 0, "operation": "sqrt"}
        )
        assert response.status_code == 400
        assert "Square root of negative number is not allowed" in response.json()["detail"]

    def test_sqrt_ignores_operand2(self, authenticated_client):
        """Test that sqrt ignores operand2: sqrt(25) = 5 regardless of operand2"""
        # Test with operand2 = 999
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 25, "operand2": 999, "operation": "sqrt"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 5.0
        assert data["operand2"] == 999  # operand2 is stored but not used
        assert data["operation"] == "sqrt"


class TestAdvancedOperationsIntegration:
    """Integration tests verifying database persistence and data integrity for advanced operations"""

    def test_advanced_operations_persist_to_database(self, authenticated_client, db_session):
        """Test that power, modulus, and sqrt calculations persist correctly to database"""
        # Create one of each advanced operation
        operations = [
            {"operand1": 2, "operand2": 8, "operation": "power", "expected": 256},
            {"operand1": 17, "operand2": 5, "operation": "modulus", "expected": 2},
            {"operand1": 64, "operand2": 0, "operation": "sqrt", "expected": 8.0}
        ]

        calc_ids = []
        for op in operations:
            response = authenticated_client.post(
                "/calculations/",
                json={"operand1": op["operand1"], "operand2": op["operand2"], "operation": op["operation"]}
            )
            assert response.status_code == 201
            calc_ids.append(response.json()["id"])

        # Verify all three are in database by querying each one
        for calc_id in calc_ids:
            db_calc = db_session.query(Calculation).filter(Calculation.id == calc_id).first()
            assert db_calc is not None
        
        # Get all calculations and verify operations
        all_calcs = db_session.query(Calculation).filter(Calculation.id.in_(calc_ids)).all()
        operations_found = {calc.operation for calc in all_calcs}
        
        assert "power" in operations_found
        assert "modulus" in operations_found
        assert "sqrt" in operations_found
        
        # Verify specific results
        power_calc = next((c for c in all_calcs if c.operation == "power"), None)
        assert power_calc is not None
        assert power_calc.result == 256
        assert power_calc.operand1 == 2
        assert power_calc.operand2 == 8

        modulus_calc = next((c for c in all_calcs if c.operation == "modulus"), None)
        assert modulus_calc is not None
        assert modulus_calc.result == 2
        assert modulus_calc.operand1 == 17
        assert modulus_calc.operand2 == 5

        sqrt_calc = next((c for c in all_calcs if c.operation == "sqrt"), None)
        assert sqrt_calc is not None
        assert sqrt_calc.result == 8.0
        assert sqrt_calc.operand1 == 64

    def test_update_calculation_to_advanced_operation(self, authenticated_client, db_session, test_user):
        """Test that existing calculations can be updated to advanced operations"""
        # Create a basic calculation
        response = authenticated_client.post(
            "/calculations/",
            json={"operand1": 10, "operand2": 5, "operation": "add"}
        )
        assert response.status_code == 201
        calc_id = response.json()["id"]

        # Update to power operation
        update_response = authenticated_client.put(
            f"/calculations/{calc_id}",
            json={"operand1": 3, "operand2": 4, "operation": "power"}
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["operation"] == "power"
        assert data["result"] == 81  # 3^4 = 81

        # Verify in database
        db_calc = db_session.query(Calculation).filter(Calculation.id == calc_id).first()
        assert db_calc.operation == "power"
        assert db_calc.result == 81

    def test_advanced_operations_calculations_correct(self, authenticated_client):
        """Test that advanced operations produce mathematically correct results"""
        test_cases = [
            # Power tests
            {"operand1": 3, "operand2": 3, "operation": "power", "expected": 27},
            {"operand1": 5, "operand2": 2, "operation": "power", "expected": 25},
            # Modulus tests
            {"operand1": 100, "operand2": 7, "operation": "modulus", "expected": 2},
            {"operand1": 50, "operand2": 8, "operation": "modulus", "expected": 2},
            # Sqrt tests
            {"operand1": 144, "operand2": 0, "operation": "sqrt", "expected": 12.0},
            {"operand1": 81, "operand2": 0, "operation": "sqrt", "expected": 9.0}
        ]

        for test in test_cases:
            response = authenticated_client.post(
                "/calculations/",
                json={
                    "operand1": test["operand1"],
                    "operand2": test["operand2"],
                    "operation": test["operation"]
                }
            )
            assert response.status_code == 201
            data = response.json()
            assert data["result"] == test["expected"], \
                f"{test['operand1']} {test['operation']} {test['operand2']} should equal {test['expected']}, got {data['result']}"

    def test_user_isolation_with_advanced_operations(self, client, db_session):
        """Test that users can only see their own advanced calculations"""
        # Create two users
        from app.auth import get_password_hash
        user1 = User(username="user1", email="user1@test.com", hashed_password=get_password_hash("password123"))
        user2 = User(username="user2", email="user2@test.com", hashed_password=get_password_hash("password123"))
        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()

        # Login as user1 and create a power calculation
        login1 = client.post("/users/login", json={"username": "user1", "password": "password123"})
        token1 = login1.json()["access_token"]
        
        response1 = client.post(
            "/calculations/",
            headers={"Authorization": f"Bearer {token1}"},
            json={"operand1": 2, "operand2": 10, "operation": "power"}
        )
        assert response1.status_code == 201
        calc1_id = response1.json()["id"]

        # Login as user2 and create a sqrt calculation
        login2 = client.post("/users/login", json={"username": "user2", "password": "password123"})
        token2 = login2.json()["access_token"]
        
        response2 = client.post(
            "/calculations/",
            headers={"Authorization": f"Bearer {token2}"},
            json={"operand1": 49, "operand2": 0, "operation": "sqrt"}
        )
        assert response2.status_code == 201

        # User1 should only see their power calculation
        browse1 = client.get("/calculations/", headers={"Authorization": f"Bearer {token1}"})
        user1_calcs = browse1.json()
        assert any(c["operation"] == "power" for c in user1_calcs)
        assert not any(c["operation"] == "sqrt" for c in user1_calcs)

        # User2 should only see their sqrt calculation
        browse2 = client.get("/calculations/", headers={"Authorization": f"Bearer {token2}"})
        user2_calcs = browse2.json()
        assert any(c["operation"] == "sqrt" for c in user2_calcs)
        assert not any(c["operation"] == "power" for c in user2_calcs)

        # User2 should not be able to access user1's calculation
        access_response = client.get(
            f"/calculations/{calc1_id}",
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert access_response.status_code == 404
