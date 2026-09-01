import pytest
import requests
import time
from utils.config import Config

@pytest.fixture(scope="session")
def api_base_url():
    return Config.API_BASE_URL if hasattr(Config, "API_BASE_URL") else "https://api.practicesoftwaretesting.com"

@pytest.fixture(scope="session")
def auth_token(api_base_url):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    
    unique_id = int(time.time())
    email = f"test_user_{unique_id}@example.com"
    password = f"SecurePass!{unique_id}99"

    # Register the new user dynamically with an address array and secure password
    register_payload = {
        "first_name": "Test",
        "last_name": "User",
        "dob": "1990-01-01",
        "address": "123 Main St",  # Will adjust if array is needed, or passed as a string/list depending on schema
        "city": "Metropolis",
        "state": "NY",
        "country": "US",
        "postcode": "10001",
        "phone": "1234567890",
        "email": email,
        "password": password
    }
    
    # The error indicated "The address field must be an array." -> let's wrap it in a list:
    register_payload["address"] = ["123 Main St"]

    reg_response = requests.post(f"{api_base_url}/users/register", json=register_payload, headers=headers)
    assert reg_response.status_code in [200, 201], f"User registration failed: {reg_response.text}"

    # Log in with the newly created user account
    login_payload = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{api_base_url}/users/login", json=login_payload, headers=headers)
    
    assert response.status_code == 200, f"Login failed with status {response.status_code}: {response.text}"
    return response.json().get("access_token")

@pytest.fixture
def auth_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }