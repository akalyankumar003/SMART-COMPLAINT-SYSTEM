import requests
import json

# 1. Login
login_res = requests.post("http://localhost:5000/api/v1/auth/login", json={
    "email": "rahul@test.com",
    "password": "user123"
})
print("Login:", login_res.status_code, login_res.text)
if login_res.status_code == 200:
    token = login_res.json()["token"]
    
    # 2. Submit complaint
    res = requests.post("http://localhost:5000/api/v1/complaints", headers={
        "Authorization": f"Bearer {token}"
    }, data={
        "category": "UPI/Payment Fraud",
        "title": "Test Title",
        "description": "Test Description",
        "incidentDate": "2026-05-03T12:00",
        "platform": "UPI App",
        "financialLoss": "5000",
        "priority": "Standard"
    })
    print("Submit:", res.status_code, res.text)
