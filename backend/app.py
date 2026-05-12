from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
import os
import sys

from extensions import mongo, jwt, socketio, bcrypt, mail

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
bcrypt.init_app(app)
jwt.init_app(app)
mail.init_app(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# MongoDB Connection with error handling
try:
    mongo.init_app(app)
    # Test connection
    # mongo.db.command('ping')
    print("✅ MongoDB connected or initializing!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {str(e)}")
    print("⚠️  Please ensure MongoDB is running and connection string is correct")
    # sys.exit(1)

# Socket.IO
socketio.init_app(app, cors_allowed_origins="*", async_mode='eventlet', logger=True, engineio_logger=True)

# Create uploads folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Register blueprints
from routes.auth import auth_bp
from routes.complaints import complaints_bp
from routes.admin import admin_bp

import routes.chat

# Mock missing ones for now
from flask import Blueprint
chat_bp = Blueprint('chat', __name__)
forum_bp = Blueprint('forum', __name__)
analytics_bp = Blueprint('analytics', __name__)
notifications_bp = Blueprint('notifications', __name__)
try:
    from routes.ai_routes import ai_bp
except ImportError:
    ai_bp = Blueprint('ai', __name__)

app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(complaints_bp, url_prefix='/api/v1/complaints')
app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
app.register_blueprint(chat_bp, url_prefix='/api/v1/chat')
app.register_blueprint(forum_bp, url_prefix='/api/v1/forum')
app.register_blueprint(analytics_bp, url_prefix='/api/v1/analytics')
app.register_blueprint(notifications_bp, url_prefix='/api/v1/notifications')
app.register_blueprint(ai_bp, url_prefix='/api/v1/ai')

# Health check endpoint
@app.route('/api/v1/health', methods=['GET'])
def health_check():
    try:
        # Ping database
        mongo.db.command('ping')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'message': 'Smart Complaint System API is running'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500

# Serve frontend static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    frontend_dir = os.path.join(app.root_path, '..', 'frontend')
    if path and os.path.exists(os.path.join(frontend_dir, path)):
        return send_from_directory(frontend_dir, path)
    return send_from_directory(frontend_dir, 'index.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Start background scheduler
try:
    from jobs.scheduler import initialize_scheduler
    initialize_scheduler(app)
except Exception as e:
    print(f"⚠️ Scheduler warning: {e}")

# Initialize database indexes
def create_indexes():
    try:
        with app.app_context():
            # Text search index on complaints
            mongo.db.complaints.create_index([('title', 'text'), ('description', 'text')])
            
            # Compound indexes for faster queries
            mongo.db.complaints.create_index([('userId', 1), ('status', 1)])
            mongo.db.complaints.create_index([('createdAt', -1)])
            mongo.db.complaints.create_index([('status', 1), ('priority', 1)])
            
            # Index on users
            mongo.db.users.create_index([('email', 1)], unique=True)
            mongo.db.users.create_index([('username', 1)], unique=True)
            
            # Index on chat messages
            mongo.db.chat_messages.create_index([('complaintId', 1), ('timestamp', -1)])
            
            # TTL index for OTP expiry
            mongo.db.otp_store.create_index([('expireAt', 1)], expireAfterSeconds=0)
            
            print("✅ Database indexes created successfully")
    except Exception as e:
        print(f"⚠️  Index creation warning: {str(e)}")

if __name__ == '__main__':
    create_indexes()
    
    print("""
    ═══════════════════════════════════════════════════════
    🛡️  SMART COMPLAINT SYSTEM - API SERVER
    ═══════════════════════════════════════════════════════
    📍 Server: http://localhost:5000
    📊 Database: MongoDB ({})
    🔐 Authentication: JWT
    💬 Real-time: Socket.IO
    ═══════════════════════════════════════════════════════
    """.format(mongo.db.name if mongo.db is not None else "Not Connected"))
    
    socketio.run(app, 
                debug=True, 
                host='0.0.0.0',
                port=5000,
                use_reloader=True)
