
import requests
import json

base_url = "http://localhost:5000/api/v1"

def test_admin_api():
    # Login
    print("Logging in...")
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    response = requests.post(f"{base_url}/auth/admin/login", json=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return

    token = response.json().get('token')
    print(f"Token acquired.")

    # Fetch complaints
    print("Fetching complaints...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{base_url}/admin/complaints", headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        complaints = response.json()
        print(f"Success! Fetched {len(complaints)} complaints.")
    else:
        print(f"Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_admin_api()
