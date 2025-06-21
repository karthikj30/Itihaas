import os

class Config:
    SECRET_KEY = 'hjshjhdjah kjshkjdhjs'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_USER')
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False
    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = False
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'website', 'static', 'uploads')
    
    # Google Maps API key
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '') 