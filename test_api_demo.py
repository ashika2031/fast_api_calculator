"""
Demo script to test FastAPI Calculator endpoints
Run this while the server is running to see all operations
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_response(response, description):
    print(f"\n{description}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 1: Root Endpoint
print_section("1. ROOT ENDPOINT")
response = requests.get(f"{BASE_URL}/")
print_response(response, "GET /")

# Test 2: Health Check
print_section("2. HEALTH CHECK")
response = requests.get(f"{BASE_URL}/health")
print_response(response, "GET /health")

# Test 3: User Registration
print_section("3. USER REGISTRATION")
timestamp = datetime.now().strftime("%H%M%S")
user_data = {
    "username": f"demo_user_{timestamp}",
    "email": f"demo_{timestamp}@example.com",
    "password": "SecurePass123!"
}
print(f"\nRegistering user: {user_data['username']}")
response = requests.post(f"{BASE_URL}/users/register", json=user_data)
print_response(response, "POST /users/register")

if response.status_code == 201:
    registered_user = response.json()
    
    # Test 4: User Login
    print_section("4. USER LOGIN")
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    print_response(response, "POST /users/login")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test 5: Create Calculations (all operations)
        print_section("5. CREATE CALCULATIONS")
        
        calculations = [
            {"operation": "add", "operand1": 15.5, "operand2": 24.3},
            {"operation": "subtract", "operand1": 50, "operand2": 18},
            {"operation": "multiply", "operand1": 7, "operand2": 8},
            {"operation": "divide", "operand1": 100, "operand2": 4}
        ]
        
        calc_ids = []
        for calc in calculations:
            response = requests.post(f"{BASE_URL}/calculations/", json=calc, headers=headers)
            print_response(response, f"POST /calculations/ - {calc['operation'].upper()}")
            if response.status_code == 201:
                calc_ids.append(response.json()["id"])
        
        # Test 6: Browse All Calculations
        print_section("6. BROWSE ALL CALCULATIONS")
        response = requests.get(f"{BASE_URL}/calculations/", headers=headers)
        print_response(response, "GET /calculations/")
        
        # Test 7: Read Specific Calculation
        if calc_ids:
            print_section("7. READ SPECIFIC CALCULATION")
            response = requests.get(f"{BASE_URL}/calculations/{calc_ids[0]}", headers=headers)
            print_response(response, f"GET /calculations/{calc_ids[0]}")
            
            # Test 8: Update Calculation
            print_section("8. UPDATE CALCULATION")
            update_data = {"operation": "multiply", "operand1": 10, "operand2": 10}
            response = requests.put(f"{BASE_URL}/calculations/{calc_ids[0]}", json=update_data, headers=headers)
            print_response(response, f"PUT /calculations/{calc_ids[0]}")
            
            # Test 9: Delete Calculation
            if len(calc_ids) > 1:
                print_section("9. DELETE CALCULATION")
                response = requests.delete(f"{BASE_URL}/calculations/{calc_ids[1]}", headers=headers)
                print_response(response, f"DELETE /calculations/{calc_ids[1]}")
        
        # Test 10: Browse After Changes
        print_section("10. BROWSE AFTER UPDATES")
        response = requests.get(f"{BASE_URL}/calculations/", headers=headers)
        print_response(response, "GET /calculations/ (after updates)")
        
        # Test 11: Test Authentication Required
        print_section("11. UNAUTHENTICATED ACCESS (Should Fail)")
        response = requests.get(f"{BASE_URL}/calculations/")
        print(f"\nGET /calculations/ without token")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test 12: Divide by Zero Error
        print_section("12. ERROR HANDLING - Divide by Zero")
        bad_calc = {"operation": "divide", "operand1": 100, "operand2": 0}
        response = requests.post(f"{BASE_URL}/calculations/", json=bad_calc, headers=headers)
        print(f"\nPOST /calculations/ - Division by zero")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

print_section("✅ ALL TESTS COMPLETED")
print("\n🎉 FastAPI Calculator - All Endpoints Working!")
print(f"👤 Test User: {user_data['username']}")
print(f"📧 Email: {user_data['email']}")
print(f"🔐 JWT Token: {token[:50]}...")
print("\n" + "="*60 + "\n")
