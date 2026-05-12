from flask import Blueprint, request, jsonify
from extensions import mongo, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import random
from datetime import datetime, timedelta
import pyotp
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    required = ['fullName', 'email', 'phone', 'state', 'username', 'password']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check username
    if mongo.db.users.find_one({'username': data['username']}):
        return jsonify({'error': 'Username already taken'}), 400
        
    if mongo.db.users.find_one({'email': data['email']}):
        return jsonify({'error': 'Email already registered'}), 400

    # Hash password
    pw_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = {
        'fullName': data['fullName'],
        'email': data['email'],
        'phone': data['phone'],
        'state': data['state'],
        'district': data.get('district', ''),
        'username': data['username'],
        'passwordHash': pw_hash,
        'securityQuestion': data.get('securityQuestion', ''),
        'securityAnswer': data.get('securityAnswer', ''),
        'role': 'user',
        'isVerified': True,
        'isActive': True,
        'isSuspended': False,
        'isFlagged': False,
        'flagReason': '',
        'twoFactorEnabled': False,
        'twoFactorSecret': '',
        'loginAttempts': 0,
        'lockoutUntil': None,
        'language': 'en',
        'createdAt': datetime.utcnow()
    }
    
    mongo.db.users.insert_one(user)
    
    # clear otp
    mongo.db.otp_store.delete_one({'email': data['email']})
    
    return jsonify({'message': 'Registered successfully'})

@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email required'}), 400
        
    otp = str(random.randint(100000, 999999))
    
    mongo.db.otp_store.update_one(
        {'email': email},
        {'$set': {'otp': otp, 'createdAt': datetime.utcnow(), 'expireAt': datetime.utcnow() + timedelta(minutes=10)}},
        upsert=True
    )
    
    # Here we would send email via flask_mail. For now, print to console.
    print(f"OTP for {email} is {otp}")
    
    return jsonify({'message': 'OTP sent successfully'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    identifier = data.get('email') or data.get('username')
    password = data.get('password')
    
    user = mongo.db.users.find_one({'$or': [{'email': identifier}, {'username': identifier}]})
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
        
    if user.get('lockoutUntil') and user['lockoutUntil'] > datetime.utcnow():
        return jsonify({'error': 'Account locked', 'lockoutUntil': user['lockoutUntil'].isoformat()}), 423
        
    if not bcrypt.check_password_hash(user['passwordHash'], password):
        attempts = user.get('loginAttempts', 0) + 1
        updates = {'loginAttempts': attempts}
        if attempts >= 5:
            updates['lockoutUntil'] = datetime.utcnow() + timedelta(minutes=30)
            
        mongo.db.users.update_one({'_id': user['_id']}, {'$set': updates})
        
        if attempts >= 5:
            return jsonify({'error': 'Account locked due to too many failed attempts'}), 423
            
        # Log failed login
        mongo.db.login_history.insert_one({
            'username': identifier,
            'ip': request.remote_addr,
            'timestamp': datetime.utcnow(),
            'success': False
        })
        return jsonify({'error': 'Invalid credentials'}), 401
        
    # Reset attempts
    mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'loginAttempts': 0, 'lockoutUntil': None}})
    
    token = create_access_token(identity=json.dumps({'id': str(user['_id']), 'email': user['email'], 'role': user['role'], 'username': user['username']}))
    
    # Log success login
    mongo.db.login_history.insert_one({
        'userId': str(user['_id']),
        'username': user['username'],
        'ip': request.remote_addr,
        'timestamp': datetime.utcnow(),
        'success': True
    })

    return jsonify({
        'token': token,
        'user': {
            'id': str(user['_id']),
            'fullName': user['fullName'],
            'email': user['email'],
            'username': user['username'],
            'role': user['role']
        }
    })

@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = mongo.db.users.find_one({'username': username})
    if not user or user.get('role') != 'admin':
        return jsonify({'error': 'Invalid admin credentials'}), 401
        
    if not bcrypt.check_password_hash(user['passwordHash'], password):
        return jsonify({'error': 'Invalid admin credentials'}), 401
        
    token = create_access_token(identity=json.dumps({'id': str(user['_id']), 'email': user['email'], 'role': user['role'], 'username': user['username']}))
    
    return jsonify({
        'token': token,
        'user': {
            'id': str(user['_id']),
            'fullName': user['fullName'],
            'email': user['email'],
            'username': user['username'],
            'role': user['role']
        }
    })

@auth_bp.route('/check-username', methods=['GET'])
def check_username():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username required'}), 400
        
    exists = mongo.db.users.find_one({'username': username}) is not None
    return jsonify({'available': not exists})

@auth_bp.route('/lock-account', methods=['POST'])
def lock_account():
    email = request.json.get('email')
    mongo.db.users.update_one(
        {'email': email},
        {'$set': {'lockoutUntil': datetime.utcnow() + timedelta(minutes=30), 'loginAttempts': 5}}
    )
    return jsonify({'message': 'Account locked'})

@auth_bp.route('/2fa/setup', methods=['POST'])
@jwt_required()
def setup_2fa():
    current_user = json.loads(get_jwt_identity())
    user = mongo.db.users.find_one({'email': current_user['email']})
    
    secret = pyotp.random_base32()
    mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'twoFactorSecret': secret}})
    
    qr_url = pyotp.totp.TOTP(secret).provisioning_uri(name=user['email'], issuer_name="SmartComplaintSystem")
    return jsonify({'secret': secret, 'qrCodeUrl': qr_url})

@auth_bp.route('/2fa/verify', methods=['POST'])
@jwt_required()
def verify_2fa():
    current_user = json.loads(get_jwt_identity())
    user = mongo.db.users.find_one({'email': current_user['email']})
    
    otp = request.json.get('otp')
    totp = pyotp.TOTP(user['twoFactorSecret'])
    
    if totp.verify(otp):
        # generate backup codes
        backup_codes = [pyotp.random_base32()[:8] for _ in range(10)]
        mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'twoFactorEnabled': True, 'backupCodes': backup_codes}})
        return jsonify({'backupCodes': backup_codes})
        
    return jsonify({'error': 'Invalid OTP'}), 400
