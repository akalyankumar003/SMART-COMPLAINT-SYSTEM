from flask import Blueprint, request, jsonify
from extensions import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

import json

admin_bp = Blueprint('admin', __name__)

def is_admin():
    try:
        identity = get_jwt_identity()
        if not identity: return False
        
        # Identity might be a JSON string or a direct dict depending on Flask-JWT version/config
        if isinstance(identity, str):
            try:
                current_user = json.loads(identity)
            except json.JSONDecodeError:
                # Fallback for legacy tokens that stored ID only
                return False
        else:
            current_user = identity
            
        return current_user.get('role') == 'admin'
    except Exception as e:
        print(f"Auth Error: {str(e)}")
        return False

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    if not is_admin(): return jsonify({'error': 'Unauthorized'}), 403
    
    total_complaints = mongo.db.complaints.count_documents({})
    pending = mongo.db.complaints.count_documents({'status': 'Pending'})
    resolved = mongo.db.complaints.count_documents({'status': 'Resolved'})
    total_users = mongo.db.users.count_documents({})
    
    return jsonify({
        'totalComplaints': total_complaints,
        'pendingComplaints': pending,
        'resolvedComplaints': resolved,
        'totalUsers': total_users
    })

@admin_bp.route('/complaints', methods=['GET'])
@jwt_required()
def get_all_complaints():
    try:
        if not is_admin(): return jsonify({'error': 'Unauthorized'}), 403
        
        status_filter = request.args.get('status')
        query = {}
        if status_filter:
            query['status'] = status_filter
            
        complaints = list(mongo.db.complaints.find(query).sort('createdAt', -1))
        
        for c in complaints:
            c['_id'] = str(c['_id'])
            
            # Safely handle userId and other ID fields
            if c.get('userId'):
                c['userId'] = str(c['userId'])
            if c.get('assignedOfficer'):
                c['assignedOfficer'] = str(c['assignedOfficer'])
                
            if 'statusHistory' in c:
                for sh in c['statusHistory']:
                    if sh.get('updatedBy'):
                        sh['updatedBy'] = str(sh['updatedBy'])
                        
            # get user info safely
            user_id = c.get('userId')
            if user_id:
                try:
                    from bson.objectid import ObjectId
                    user_id_query = ObjectId(user_id) if len(user_id) == 24 else user_id
                    user = mongo.db.users.find_one({'_id': user_id_query})
                    if user:
                        c['userName'] = user.get('fullName', 'Unknown User')
                        c['userEmail'] = user.get('email', 'N/A')
                    else:
                        c['userName'] = 'User Not Found'
                        c['userEmail'] = 'N/A'
                except Exception:
                    c['userName'] = 'Invalid User ID'
                    c['userEmail'] = 'N/A'
            else:
                c['userName'] = 'Anonymous'
                c['userEmail'] = 'N/A'
                
        return jsonify(complaints)
    except Exception as e:
        print(f"CRITICAL ERROR in get_all_complaints: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/audit-logs', methods=['GET'])
@jwt_required()
def get_audit_logs():
    if not is_admin(): return jsonify({'error': 'Unauthorized'}), 403
    logs = list(mongo.db.audit_logs.find().sort('timestamp', -1).limit(100))
    for l in logs:
        l['_id'] = str(l['_id'])
    return jsonify(logs)

@admin_bp.route('/complaints/stats/extended', methods=['GET'])
@jwt_required()
def get_extended_stats():
    if not is_admin(): return jsonify({'error': 'Unauthorized'}), 403
    
    total = mongo.db.complaints.count_documents({})
    # Mock SLA breach data
    sla_breached = mongo.db.complaints.count_documents({'status': {'$ne': 'Resolved'}, 'priority': 'High'})
    
    # Mock CSAT
    ratings = list(mongo.db.complaints.find({'rating': {'$exists': True}}, {'rating': 1}))
    avg_rating = sum([r.get('rating', 0) for r in ratings]) / len(ratings) if ratings else 4.2
    
    return jsonify({
        'slaBreachRate': (sla_breached / total * 100) if total > 0 else 0,
        'avgCSAT': round(avg_rating, 1),
        'totalRevenue': 249800 # Placeholder for financial analytics
    })

@admin_bp.route('/complaints/<id>/status', methods=['PUT'])
@jwt_required()
def update_status(id):
    if not is_admin(): return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    status = data.get('status')
    note = data.get('note', '')
    
    from bson.objectid import ObjectId
    mongo.db.complaints.update_one(
        {'_id': ObjectId(id)},
        {
            '$set': {'status': status},
            '$push': {'statusHistory': {'status': status, 'note': note, 'updatedAt': datetime.utcnow()}}
        }
    )
    
    # Send Notification to User
    complaint = mongo.db.complaints.find_one({'_id': ObjectId(id)})
    if complaint and complaint.get('userId'):
        mongo.db.notifications.insert_one({
            'userId': complaint['userId'],
            'complaintId': complaint['complaintId'],
            'title': f'Complaint {status}',
            'message': f'Your complaint {complaint["complaintId"]} has been updated to: {status}. Note: {note}',
            'type': status.lower(),
            'isRead': False,
            'createdAt': datetime.utcnow()
        })
    
    return jsonify({'message': 'Status updated'})

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        if not is_admin(): return jsonify({'error': 'Unauthorized'}), 403
        
        users = list(mongo.db.users.find({}, {'passwordHash': 0, 'securityQuestions': 0}).sort('createdAt', -1))
        for u in users:
            u['_id'] = str(u['_id'])
            if 'createdAt' in u and u['createdAt']:
                if isinstance(u['createdAt'], datetime):
                    u['createdAt'] = u['createdAt'].isoformat()
            
        return jsonify(users)
    except Exception as e:
        print(f"ERROR in get_users: {str(e)}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<id>/suspend', methods=['POST'])
@jwt_required()
def suspend_user(id):
    if not is_admin(): return jsonify({'error': 'Unauthorized'}), 403
    
    from bson.objectid import ObjectId
    mongo.db.users.update_one(
        {'_id': ObjectId(id)},
        {'$set': {'isSuspended': True}}
    )
    return jsonify({'message': 'User suspended'})

@admin_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    if not is_admin(): return jsonify({'error': 'Unauthorized'}), 403
    data = request.json
    admin_id = json.loads(get_jwt_identity())['id']
    
    mongo.db.users.update_one(
        {'_id': ObjectId(admin_id)},
        {'$set': {
            'fullName': data.get('fullName'),
            'email': data.get('email')
        }}
    )
    return jsonify({'message': 'Profile updated'})

def log_action(admin_id, action, target_id, details=""):
    from datetime import datetime
    mongo.db.audit_logs.insert_one({
        'adminId': admin_id,
        'action': action,
        'targetId': target_id,
        'details': details,
        'timestamp': datetime.utcnow()
    })
