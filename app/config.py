import os

class Config:
    # Database configuration
    ENV = 'development'  # ✅ Add this line
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:rakesh1327@localhost/university_timetable'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable SQLAlchemy event notifications

    # Flask secret key for session management and CSRF protection
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    TESTING = False