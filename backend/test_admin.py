import requests

res = requests.post("http://localhost:5000/api/v1/auth/admin/login", json={
    "username": "admin",
    "password": "admin"
})
print(res.status_code, res.text)
