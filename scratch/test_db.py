from extensions import mongo
from app import app
with app.app_context():
    user = mongo.db.users.find_one({'username': 'surya'}) or mongo.db.users.find_one({'email': 'surya@test.com'}) or list(mongo.db.users.find({'role': 'user'}))[0]
    print("User ID:", str(user['_id']))
    complaints = list(mongo.db.complaints.find({'userId': str(user['_id'])}))
    print("Complaints with str userId:", len(complaints))
    from bson.objectid import ObjectId
    complaints = list(mongo.db.complaints.find({'userId': user['_id']}))
    print("Complaints with ObjectId userId:", len(complaints))
    import json
    from bson import json_util
    print(json.loads(json_util.dumps(complaints)))
