import os
from datetime import timedelta

class Config:
    # Secret Keys
    SECRET_KEY = os.environ.get('SECRET_KEY', 'scs-secret-key-change-in-production-2025')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'scs-jwt-secret-change-2025')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    
    # MongoDB Connection
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/smartcomplaintsystem')
    # For MongoDB Atlas (cloud):
    # MONGO_URI = 'mongodb+srv://username:password@cluster.mongodb.net/smartcomplaintsystem?retryWrites=true&w=majority'
    
    # File Upload
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt', 'mp4', 'avi', 'mov'}
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'your-app-password')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@smartcomplaintsystem.gov.in')
    
    # SMS Configuration (Twilio)
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')
    
    # AI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    AI_MODEL = 'gpt-3.5-turbo'
    AI_TEMPERATURE = 0.7
