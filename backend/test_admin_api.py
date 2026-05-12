import requests

res = requests.post("http://localhost:5000/api/v1/auth/admin/login", json={
    "username": "admin",
    "password": "admin"
})
token = res.json()["token"]

res = requests.get("http://localhost:5000/api/v1/admin/complaints", headers={
    "Authorization": f"Bearer {token}"
})
print("Admin Complaints:", res.status_code, res.text)
