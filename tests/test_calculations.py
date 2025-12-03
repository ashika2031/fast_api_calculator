import pytest
from fastapi import status


def test_create_calculation_success(authenticated_client):
    """Test successful calculation creation."""
    calculation_data = {
        "operation": "add",
        "operand1": 10,
        "operand2": 5
    }
    
    response = authenticated_client.post("/calculations/", json=calculation_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["operation"] == "add"
    assert data["operand1"] == 10
    assert data["operand2"] == 5
    assert data["result"] == 15
    assert "id" in data
    assert "created_at" in data


def test_create_calculation_all_operations(authenticated_client):
    """Test all calculation operations."""
    operations = [
        {"operation": "add", "operand1": 10, "operand2": 5, "expected": 15},
        {"operation": "subtract", "operand1": 10, "operand2": 5, "expected": 5},
        {"operation": "multiply", "operand1": 10, "operand2": 5, "expected": 50},
        {"operation": "divide", "operand1": 10, "operand2": 5, "expected": 2},
    ]
    
    for op in operations:
        response = authenticated_client.post("/calculations/", json={
            "operation": op["operation"],
            "operand1": op["operand1"],
            "operand2": op["operand2"]
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["result"] == op["expected"]


def test_create_calculation_divide_by_zero(authenticated_client):
    """Test division by zero error."""
    calculation_data = {
        "operation": "divide",
        "operand1": 10,
        "operand2": 0
    }
    
    response = authenticated_client.post("/calculations/", json=calculation_data)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Division by zero" in response.json()["detail"]


def test_create_calculation_invalid_operation(authenticated_client):
    """Test invalid operation."""
    calculation_data = {
        "operation": "invalid",
        "operand1": 10,
        "operand2": 5
    }
    
    response = authenticated_client.post("/calculations/", json=calculation_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_calculation_modulo(authenticated_client):
    """Test unsupported modulo operation to trigger error path."""
    # This tests the error path in perform_calculation for unsupported operations
    # We'll use a valid schema but the function should handle it
    from app.routers.calculations import perform_calculation
    import pytest
    from fastapi import HTTPException
    
    # Test the function directly to reach the else branch
    with pytest.raises(HTTPException) as exc_info:
        perform_calculation("modulo", 10, 3)
    
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid operation" in str(exc_info.value.detail)


def test_create_calculation_unauthenticated(client):
    """Test calculation creation without authentication."""
    calculation_data = {
        "operation": "add",
        "operand1": 10,
        "operand2": 5
    }
    
    response = client.post("/calculations/", json=calculation_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_browse_calculations(authenticated_client):
    """Test browsing all calculations."""
    # Create multiple calculations
    calculations_data = [
        {"operation": "add", "operand1": 10, "operand2": 5},
        {"operation": "subtract", "operand1": 20, "operand2": 8},
        {"operation": "multiply", "operand1": 3, "operand2": 7}
    ]
    
    for calc in calculations_data:
        authenticated_client.post("/calculations/", json=calc)
    
    # Browse calculations
    response = authenticated_client.get("/calculations/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3


def test_browse_calculations_empty(authenticated_client):
    """Test browsing calculations when none exist."""
    response = authenticated_client.get("/calculations/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_read_calculation_success(authenticated_client):
    """Test reading a specific calculation."""
    # Create a calculation
    calc_data = {"operation": "add", "operand1": 10, "operand2": 5}
    create_response = authenticated_client.post("/calculations/", json=calc_data)
    calc_id = create_response.json()["id"]
    
    # Read the calculation
    response = authenticated_client.get(f"/calculations/{calc_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == calc_id
    assert data["operation"] == "add"
    assert data["result"] == 15


def test_read_calculation_not_found(authenticated_client):
    """Test reading a non-existent calculation."""
    response = authenticated_client.get("/calculations/99999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"]


def test_edit_calculation_success(authenticated_client):
    """Test editing a calculation."""
    # Create a calculation
    calc_data = {"operation": "add", "operand1": 10, "operand2": 5}
    create_response = authenticated_client.post("/calculations/", json=calc_data)
    calc_id = create_response.json()["id"]
    
    # Edit the calculation
    update_data = {"operation": "multiply", "operand1": 10, "operand2": 5}
    response = authenticated_client.put(f"/calculations/{calc_id}", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["operation"] == "multiply"
    assert data["result"] == 50


def test_edit_calculation_partial_update(authenticated_client):
    """Test partial update of a calculation."""
    # Create a calculation
    calc_data = {"operation": "add", "operand1": 10, "operand2": 5}
    create_response = authenticated_client.post("/calculations/", json=calc_data)
    calc_id = create_response.json()["id"]
    
    # Update only operand1
    update_data = {"operand1": 20}
    response = authenticated_client.put(f"/calculations/{calc_id}", json=update_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["operand1"] == 20
    assert data["operand2"] == 5
    assert data["result"] == 25


def test_edit_calculation_not_found(authenticated_client):
    """Test editing a non-existent calculation."""
    update_data = {"operation": "multiply"}
    response = authenticated_client.put("/calculations/99999", json=update_data)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_calculation_success(authenticated_client):
    """Test deleting a calculation."""
    # Create a calculation
    calc_data = {"operation": "add", "operand1": 10, "operand2": 5}
    create_response = authenticated_client.post("/calculations/", json=calc_data)
    calc_id = create_response.json()["id"]
    
    # Delete the calculation
    response = authenticated_client.delete(f"/calculations/{calc_id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's deleted
    get_response = authenticated_client.get(f"/calculations/{calc_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_calculation_not_found(authenticated_client):
    """Test deleting a non-existent calculation."""
    response = authenticated_client.delete("/calculations/99999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_user_isolation(client, test_user, test_user2):
    """Test that users can only access their own calculations."""
    # Register and login first user
    client.post("/users/register", json=test_user)
    login_response = client.post("/users/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token1 = login_response.json()["access_token"]
    
    # Create calculation for first user
    client.headers = {"Authorization": f"Bearer {token1}"}
    calc_response = client.post("/calculations/", json={
        "operation": "add",
        "operand1": 10,
        "operand2": 5
    })
    calc_id = calc_response.json()["id"]
    
    # Register and login second user
    client.post("/users/register", json=test_user2)
    login_response2 = client.post("/users/login", json={
        "username": test_user2["username"],
        "password": test_user2["password"]
    })
    token2 = login_response2.json()["access_token"]
    
    # Try to access first user's calculation with second user's token
    client.headers = {"Authorization": f"Bearer {token2}"}
    response = client.get(f"/calculations/{calc_id}")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
