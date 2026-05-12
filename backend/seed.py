from app import app, mongo, bcrypt
from datetime import datetime, timedelta
import random
from bson import ObjectId

def seed_database():
    """Seed database with admin user and test data"""
    
    print("""
    ═══════════════════════════════════════════════════════
    🌱 SEEDING DATABASE - SMART COMPLAINT SYSTEM
    ═══════════════════════════════════════════════════════
    """)
    
    with app.app_context():
        # Clear existing data (only in development)
        print("🗑️  Clearing existing data...")
        mongo.db.users.delete_many({})
        mongo.db.complaints.delete_many({})
        mongo.db.evidence.delete_many({})
        mongo.db.forum_posts.delete_many({})
        mongo.db.notifications.delete_many({})
        print("  ✅ Data cleared\n")
        
        # Create admin user
        print("👨💼 Creating admin user...")
        admin_hash = bcrypt.generate_password_hash('admin').decode('utf-8')
        admin = {
            'fullName': 'System Administrator',
            'email': 'admin@scs.gov.in',
            'username': 'admin',
            'phone': '+919000000000',
            'state': 'Delhi',
            'district': 'New Delhi',
            'role': 'admin',
            'passwordHash': admin_hash,
            'isActive': True,
            'isSuspended': False,
            'isFlagged': False,
            'isVerified': True,
            'loginAttempts': 0,
            'twoFactorEnabled': False,
            'language': 'en',
            'emailNotifications': True,
            'smsNotifications': True,
            'pushNotifications': True,
            'sessions': [],
            'createdAt': datetime.utcnow()
        }
        admin_result = mongo.db.users.insert_one(admin)
        print(f"  ✅ Admin created: admin@scs.gov.in / admin\n")
        
        # Create test users
        print("👥 Creating test users...")
        user_hash = bcrypt.generate_password_hash('user123').decode('utf-8')
        test_users = [
            {
                'fullName': 'Rahul Sharma',
                'email': 'rahul@test.com',
                'username': 'rahul_sharma',
                'phone': '+919876543210',
                'state': 'Maharashtra',
                'district': 'Mumbai'
            },
            {
                'fullName': 'Priya Patel',
                'email': 'priya@test.com',
                'username': 'priya_patel',
                'phone': '+918765432109',
                'state': 'Gujarat',
                'district': 'Ahmedabad'
            },
            {
                'fullName': 'Amit Kumar',
                'email': 'amit@test.com',
                'username': 'amit_kumar',
                'phone': '+917654321098',
                'state': 'Uttar Pradesh',
                'district': 'Lucknow'
            },
        ]
        
        user_ids = []
        for u in test_users:
            u.update({
                'passwordHash': user_hash,
                'role': 'user',
                'isActive': True,
                'isSuspended': False,
                'isFlagged': False,
                'isVerified': True,
                'loginAttempts': 0,
                'twoFactorEnabled': False,
                'language': 'en',
                'emailNotifications': True,
                'smsNotifications': False,
                'pushNotifications': True,
                'sessions': [],
                'createdAt': datetime.utcnow()
            })
        
        result = mongo.db.users.insert_many(test_users)
        user_ids = result.inserted_ids
        print(f"  ✅ Created {len(test_users)} test users")
        print("  📧 Test login: rahul@test.com / user123\n")
        
        # Create sample complaints
        print("📋 Creating sample complaints...")
        categories = [
            'UPI/Payment Fraud',
            'Account Hacking',
            'Online Job Scam',
            'Phishing Attack',
            'Ransomware',
            'Identity Theft',
            'Social Media Crime',
            'E-Commerce Fraud',
            'Cyberbullying',
            'Cryptocurrency Scam',
            'Email Fraud',
            'Data Breach',
            'Mobile App Fraud',
            'Banking Cyber Fraud'
        ]
        
        statuses = ['Pending', 'Under Review', 'In Progress', 'Resolved']
        priorities = ['Standard', 'High', 'Critical']
        platforms = ['UPI App', 'Social Media', 'Email', 'WhatsApp', 'Website', 'Mobile App']
        
        complaints = []
        for i in range(20):
            category = random.choice(categories)
            status = random.choice(statuses)
            priority = random.choice(priorities)
            user_id = random.choice(user_ids)
            days_ago = random.randint(1, 60)
            
            complaint = {
                'complaintId': f'SCS-2025-{str(i+1).zfill(5)}',
                'userId': user_id,
                'category': category,
                'title': f'Sample {category} complaint - Case #{i+1}',
                'description': f'This is a detailed description of a {category} incident. The incident occurred when I received a suspicious message/call asking for my personal information. I lost approximately ₹{random.randint(1000, 100000)} in this incident. I am filing this complaint to seek help and recover my losses.',
                'incidentDate': (datetime.utcnow() - timedelta(days=days_ago + random.randint(1, 10))).isoformat(),
                'platform': random.choice(platforms),
                'specificPlatform': random.choice(['GPay', 'PhonePe', 'Paytm', 'Instagram', 'Facebook', 'WhatsApp']),
                'suspectName': random.choice(['', 'Unknown', 'John Doe', 'Fake Seller']),
                'suspectPhone': random.choice(['', '+919999999999', '+918888888888']),
                'suspectEmail': random.choice(['', 'scammer@fake.com', 'unknown@example.com']),
                'financialLoss': random.choice([0, 5000, 15000, 30000, 50000, 75000, 100000]),
                'priority': priority,
                'status': status,
                'escalationLevel': 0,
                'assignedOfficer': admin_result.inserted_id if status != 'Pending' else None,
                'statusHistory': [
                    {
                        'status': 'Pending',
                        'note': 'Complaint filed successfully',
                        'updatedBy': user_id,
                        'updatedAt': (datetime.utcnow() - timedelta(days=days_ago)).isoformat()
                    }
                ],
                'language': 'en',
                'evidenceSecured': random.choice([True, False]),
                'impactScore': random.randint(20, 95),
                'linkedComplaints': [],
                'reminderDate': None,
                'reminderActive': False,
                'emailNotify': True,
                'smsNotify': False,
                'createdAt': datetime.utcnow() - timedelta(days=days_ago),
                'updatedAt': datetime.utcnow() - timedelta(days=random.randint(0, days_ago))
            }
            
            # Add more status history for non-pending complaints
            if status != 'Pending':
                complaint['statusHistory'].append({
                    'status': 'Under Review',
                    'note': 'Complaint is being reviewed by our team',
                    'updatedBy': admin_result.inserted_id,
                    'updatedAt': (datetime.utcnow() - timedelta(days=days_ago-5)).isoformat()
                })
            
            if status in ['In Progress', 'Resolved']:
                complaint['statusHistory'].append({
                    'status': 'In Progress',
                    'note': 'Investigation has been initiated',
                    'updatedBy': admin_result.inserted_id,
                    'updatedAt': (datetime.utcnow() - timedelta(days=days_ago-10)).isoformat()
                })
            
            if status == 'Resolved':
                complaint['statusHistory'].append({
                    'status': 'Resolved',
                    'note': 'Case has been successfully resolved. Recovery process initiated.',
                    'updatedBy': admin_result.inserted_id,
                    'updatedAt': (datetime.utcnow() - timedelta(days=random.randint(0, 5))).isoformat()
                })
            
            complaints.append(complaint)
        
        mongo.db.complaints.insert_many(complaints)
        print(f"  ✅ Created {len(complaints)} sample complaints\n")
        
        # Create forum posts
        print("💬 Creating forum posts...")
        forum_categories = ['Scam Alerts', 'Prevention Tips', 'Success Stories', 'Ask Community']
        for i in range(8):
            post = {
                'userId': random.choice(user_ids),
                'title': f'Important cybersecurity tip #{i+1}',
                'content': f'Here is some valuable advice about protecting yourself from cyber crimes. Stay vigilant and always verify before sharing personal information. Report suspicious activities immediately.',
                'category': random.choice(forum_categories),
                'upvotes': random.randint(5, 100),
                'downvotes': random.randint(0, 10),
                'commentCount': random.randint(0, 15),
                'isAnonymous': random.choice([True, False]),
                'anonymousHandle': f'CyberUser#{random.randint(1000, 9999)}',
                'isPinned': i == 0,
                'isModerated': True,
                'isReported': False,
                'createdAt': datetime.utcnow() - timedelta(days=random.randint(0, 30))
            }
            mongo.db.forum_posts.insert_one(post)
        print(f"  ✅ Created 8 forum posts\n")
        
        # Create sample notifications for test users
        print("🔔 Creating sample notifications...")
        notification_types = ['status_change', 'admin_message', 'reminder', 'system']
        for user_id in user_ids[:2]:  # Only for first 2 users
            for i in range(3):
                notification = {
                    'userId': user_id,
                    'type': random.choice(notification_types),
                    'title': f'Notification {i+1}',
                    'message': f'This is a sample notification message about your complaint status.',
                    'link': f'/complaint-detail.html?id={ObjectId()}',
                    'isRead': random.choice([True, False]),
                    'createdAt': datetime.utcnow() - timedelta(hours=random.randint(1, 48))
                }
                mongo.db.notifications.insert_one(notification)
        print(f"  ✅ Created sample notifications\n")
        
        print("""
        ═══════════════════════════════════════════════════════
        ✅ DATABASE SEEDING COMPLETE!
        ═══════════════════════════════════════════════════════
        
        📊 Summary:
           • Admin Account: admin@scs.gov.in / admin
           • Test Users: 3 (password: user123)
           • Sample Complaints: 20
           • Forum Posts: 8
           • Notifications: Created
        
        🚀 You can now start the application!
        ═══════════════════════════════════════════════════════
        """)

if __name__ == '__main__':
    seed_database()
