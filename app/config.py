import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:rakesh1327@localhost/university_timetable'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Generate a strong secret key if not provided
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(24).hex()
    
    # Session configuration
    TESTING = False
    SESSION_COOKIE_SECURE = False  # Set to True in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    SESSION_REFRESH_EACH_REQUEST = True