from app import app, mongo
from datetime import datetime

def initialize_collections():
    """Create all MongoDB collections with validators"""
    
    print("📦 Initializing MongoDB collections...")
    
    # Collections to create
    collections = [
        'users',
        'complaints',
        'evidence',
        'chat_messages',
        'forum_posts',
        'forum_comments',
        'notifications',
        'admin_roles',
        'audit_logs',
        'email_templates',
        'fraud_alerts',
        'contact_messages',
        'settings',
        'otp_store'
    ]
    
    with app.app_context():
        existing_collections = mongo.db.list_collection_names()
        
        for collection_name in collections:
            if collection_name not in existing_collections:
                mongo.db.create_collection(collection_name)
                print(f"  ✅ Created collection: {collection_name}")
            else:
                print(f"  ℹ️  Collection already exists: {collection_name}")
        
        # Initialize settings collection with default values
        if mongo.db.settings.count_documents({}) == 0:
            default_settings = {
                'key': 'system_settings',
                'systemName': 'Smart Complaint System',
                'contactEmail': 'support@smartcomplaintsystem.gov.in',
                'maintenanceMode': False,
                'maxUploadSize': 52428800,  # 50MB in bytes
                'allowedFileTypes': ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt', 'mp4', 'avi'],
                'jwtExpiry': 24,  # hours
                'updatedAt': datetime.utcnow()
            }
            mongo.db.settings.insert_one(default_settings)
            print("  ✅ Initialized default system settings")
        
        print("✅ Database initialization complete!\n")

if __name__ == '__main__':
    initialize_collections()
