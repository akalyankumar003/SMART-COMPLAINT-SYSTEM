from app import app
from flask_jwt_extended import create_access_token
import json
from extensions import mongo

with app.app_context():
    user = mongo.db.users.find_one({'username': 'surya'})
    if not user:
        user = list(mongo.db.users.find({'role': 'user'}))[0]
    
    token = create_access_token(identity=json.dumps({'id': str(user['_id']), 'email': user['email'], 'role': user['role'], 'username': user['username']}))
    with app.test_client() as client:
        res = client.get('/api/v1/complaints?limit=50', headers={'Authorization': f'Bearer {token}'})
        print("STATUS:", res.status_code)
        print("DATA:", res.data)
