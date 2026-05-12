from flask import Blueprint, request, jsonify
from extensions import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

import json

complaints_bp = Blueprint('complaints', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@complaints_bp.route('', methods=['POST'])
@jwt_required()
def create_complaint():
    current_user = json.loads(get_jwt_identity())
    user_id = current_user['id']
    
    # Handle Form Data
    title = request.form.get('title')
    category = request.form.get('category')
    description = request.form.get('description')
    incidentDate = request.form.get('incidentDate')
    platform = request.form.get('platform')
    financialLoss = int(request.form.get('financialLoss') or 0)
    priority = request.form.get('priority', 'Standard')
    
    # AI Fields
    isAIAssisted = request.form.get('isAIAssisted') == 'true'
    aiConfidenceScore = request.form.get('aiConfidenceScore', type=int)
    
    try:
        legalSections = json.loads(request.form.get('legalSections', '[]'))
    except:
        legalSections = []
        
    try:
        suggestedEvidence = json.loads(request.form.get('suggestedEvidence', '[]'))
    except:
        suggestedEvidence = []
    # Files
    files = request.files.getlist('file')
    evidence_list = []
    
    for file in files:
        if file.filename == '': continue
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(filepath)
        
        evidence = {
            'userId': user_id,
            'originalFilename': filename,
            'storedFilename': unique_name,
            'fileSize': os.path.getsize(filepath),
            'uploadedAt': datetime.utcnow()
        }
        mongo.db.evidence.insert_one(evidence)
        evidence_list.append(str(evidence['_id']))

    # Generate Complaint ID
    count = mongo.db.complaints.count_documents({})
    complaint_id = f"SCS-{datetime.utcnow().year}-{str(count+1).zfill(5)}"
    
    # Impact Score mock calculation
    impact_score = min(100, int((financialLoss / 10000) * 10 + len(evidence_list) * 5 + 20))
    
    complaint = {
        'complaintId': complaint_id,
        'userId': user_id,
        'title': title,
        'category': category,
        'description': description,
        'incidentDate': incidentDate,
        'platform': platform,
        'financialLoss': financialLoss,
        'priority': priority,
        'status': 'Pending',
        'evidence': evidence_list,
        'impactScore': impact_score,
        'statusHistory': [{
            'status': 'Pending',
            'note': 'Complaint filed successfully',
            'updatedAt': datetime.utcnow()
        }],
        'isAIAssisted': isAIAssisted,
        'aiConfidenceScore': aiConfidenceScore,
        'legalSections': legalSections,
        'suggestedEvidence': suggestedEvidence,
        'createdAt': datetime.utcnow()
    }
    
    result = mongo.db.complaints.insert_one(complaint)
    return jsonify({'complaintId': complaint_id, '_id': str(result.inserted_id)})

@complaints_bp.route('', methods=['GET'])
@jwt_required()
def get_complaints():
    current_user = json.loads(get_jwt_identity())
    user_id = current_user['id']
    limit = int(request.args.get('limit', 10))
    
    from bson.objectid import ObjectId
    query = {'$or': [{'userId': user_id}, {'userId': ObjectId(user_id)}]}
    complaints = list(mongo.db.complaints.find(query).sort('createdAt', -1).limit(limit))
    
    # Clean up ObjectIds for JSON serialization
    for c in complaints:
        c['_id'] = str(c['_id'])
        if 'userId' in c and c['userId']:
            c['userId'] = str(c['userId'])
        if 'assignedOfficer' in c and c['assignedOfficer']:
            c['assignedOfficer'] = str(c['assignedOfficer'])
        if 'statusHistory' in c:
            for sh in c['statusHistory']:
                if 'updatedBy' in sh and sh['updatedBy']:
                    sh['updatedBy'] = str(sh['updatedBy'])
    
    return jsonify(complaints)

@complaints_bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_complaint(id):
    current_user = json.loads(get_jwt_identity())
    user_id = current_user['id']
    
    from bson.objectid import ObjectId
    try:
        obj_id = ObjectId(id)
        query = {'_id': obj_id}
    except:
        query = {'complaintId': id}
        
    complaint = mongo.db.complaints.find_one(query)
    
    if not complaint:
        # Check if user is admin (optional, but good for detail view)
        if current_user.get('role') == 'admin':
            complaint = mongo.db.complaints.find_one({'_id': ObjectId(id)})
            
    if not complaint:
        return jsonify({'error': 'Complaint not found'}), 404
        
    complaint['_id'] = str(complaint['_id'])
    if 'userId' in complaint:
        complaint['userId'] = str(complaint['userId'])
    if 'assignedOfficer' in complaint and complaint['assignedOfficer']:
        complaint['assignedOfficer'] = str(complaint['assignedOfficer'])
    if 'statusHistory' in complaint:
        for sh in complaint['statusHistory']:
            if 'updatedBy' in sh and sh['updatedBy']:
                sh['updatedBy'] = str(sh['updatedBy'])
                
    return jsonify(complaint)

@complaints_bp.route('/check-duplicate', methods=['POST'])
@jwt_required()
def check_duplicate():
    data = request.json
    title = data.get('title', '').lower()
    description = data.get('description', '').lower()
    
    # Simple keyword-based semantic matching
    keywords = set(title.split() + description.split())
    
    from bson.objectid import ObjectId
    # Find recently filed complaints
    others = list(mongo.db.complaints.find({}).sort('createdAt', -1).limit(50))
    
    matches = []
    for o in others:
        o_text = (o.get('title', '') + " " + o.get('description', '')).lower()
        o_keywords = set(o_text.split())
        
        intersection = keywords.intersection(o_keywords)
        if len(intersection) > 3: # Simple threshold
            matches.append({
                'id': str(o['_id']),
                'complaintId': o.get('complaintId'),
                'title': o.get('title'),
                'similarity': round((len(intersection) / len(keywords)) * 100, 1)
            })
            
    return jsonify({'matches': sorted(matches, key=lambda x: x['similarity'], reverse=True)[:3]})

@complaints_bp.route('/<id>/withdraw', methods=['PUT'])
@jwt_required()
def withdraw(id):
    current_user = json.loads(get_jwt_identity())
    
    from bson.objectid import ObjectId
    query = {
        '_id': ObjectId(id),
        '$or': [{'userId': current_user['id']}, {'userId': ObjectId(current_user['id'])}]
    }
    complaint = mongo.db.complaints.find_one(query)
    if not complaint:
        return jsonify({'error': 'Not found or unauthorized'}), 404
        
    if complaint['status'] not in ['Pending', 'Under Review']:
        return jsonify({'error': 'Cannot withdraw at this stage'}), 400
        
    mongo.db.complaints.update_one(
        {'_id': ObjectId(id)},
        {
            '$set': {'status': 'Withdrawn'},
            '$push': {'statusHistory': {'status': 'Withdrawn', 'note': 'Withdrawn by user', 'updatedAt': datetime.utcnow()}}
        }
    )
    return jsonify({'message': 'Complaint withdrawn'})

@complaints_bp.route('/<id>/rating', methods=['POST'])
@jwt_required()
def submit_rating(id):
    data = request.json
    rating = data.get('rating')
    
    from bson.objectid import ObjectId
    mongo.db.complaints.update_one(
        {'_id': ObjectId(id)},
        {'$set': {'rating': rating}}
    )
    return jsonify({'message': 'Rating submitted'})
