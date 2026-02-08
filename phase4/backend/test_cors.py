import requests
import json

# Test the signup endpoint with proper CORS headers
url = "http://localhost:8000/api/auth/signup"

# Headers that simulate a frontend request
headers = {
    "Content-Type": "application/json",
    "Origin": "http://localhost:3000",
    "Referer": "http://localhost:3000/",
}

# Test data
data = {
    "email": "testcors@example.com",
    "password": "password123",
    "first_name": "TestCORS",
    "last_name": "User"
}

print("Testing signup endpoint with CORS headers...")
try:
    response = requests.options(url, headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type"
    })
    print(f"OPTIONS response status: {response.status_code}")
    print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
    print(f"Access-Control-Allow-Credentials: {response.headers.get('Access-Control-Allow-Credentials')}")
    print(f"Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods')}")
    print(f"Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers')}")

    # Now test the actual POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"\nPOST response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    print(f"Response body: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")