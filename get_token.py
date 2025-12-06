#!/usr/bin/env python3
"""Quick script to register a user and get a JWT token for Swagger UI testing."""

import requests
import json

BASE_URL = "http://localhost:8000"

# User credentials
user_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123"
}

print("🔐 FastAPI Calculator - Token Generator\n")
print("=" * 50)

# Try to register user
print("\n1️⃣  Registering user...")
try:
    response = requests.post(f"{BASE_URL}/users/register", json=user_data)
    if response.status_code == 201:
        print("✅ User registered successfully!")
        print(f"   User ID: {response.json()['id']}")
    elif response.status_code == 400:
        print("ℹ️  User already exists, proceeding to login...")
    else:
        print(f"⚠️  Registration response: {response.status_code}")
except Exception as e:
    print(f"❌ Registration error: {e}")

# Login to get token
print("\n2️⃣  Logging in to get JWT token...")
try:
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        
        print("✅ Login successful!\n")
        print("=" * 50)
        print("📋 COPY THIS FOR SWAGGER UI AUTHORIZATION:")
        print("=" * 50)
        print(f"\nBearer {access_token}\n")
        print("=" * 50)
        print("\n📝 Instructions:")
        print("1. Click the green 'Authorize' button in Swagger UI")
        print("2. Paste the token above (including 'Bearer ') in the 'Value' field")
        print("3. Click 'Authorize' then 'Close'")
        print("4. Now you can test all protected endpoints!")
        print("\n" + "=" * 50)
        
        # Test the token
        print("\n3️⃣  Testing token by creating a calculation...")
        headers = {"Authorization": f"Bearer {access_token}"}
        calc_data = {
            "operation": "add",
            "operand1": 10,
            "operand2": 5
        }
        response = requests.post(f"{BASE_URL}/calculations/", json=calc_data, headers=headers)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Token works! Calculation result: {result['operand1']} + {result['operand2']} = {result['result']}")
        else:
            print(f"⚠️  Calculation test status: {response.status_code}")
            
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ Login error: {e}")

print("\n✨ Done! Use the token above in Swagger UI.\n")
