
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from backend.app import app
from backend.extensions import mongo

with app.app_context():
    user = mongo.db.users.find_one({'username': 'admin'})
    if user:
        print(f"ID: {user['_id']}")
        print(f"Username: {user['username']}")
        print(f"Role: {user['role']}")
    else:
        print("Admin user not found")
