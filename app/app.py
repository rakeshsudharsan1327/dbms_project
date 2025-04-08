from flask import Flask, send_from_directory, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv
from app.config import Config
from app.swagger import swaggerui_blueprint, SWAGGER_URL
from app.routes.staff_routes import staff_bp
from app.routes.course_routes import course_bp
from app.routes.class_routes import class_bp
from app.routes.timetable_routes import timetable_bp
from app.services.auth import auth_bp
from app.models.user_model import User
from app.extensions import db, socketio
from app.routes.home import home_bp  # Add home blueprint
import logging
import os
import time
from datetime import timedelta

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)
    CORS(app)
    
    # Enhanced session security configuration
    app.config.update(
        SESSION_COOKIE_SECURE=not app.debug,  # True in production
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
        SESSION_REFRESH_EACH_REQUEST=True
    )
    
    @app.before_request
    def before_request():
        # Initialize session if needed
        if not session.get('_permanent', False):
            session.permanent = True
            
        # Generate CSRF token for authenticated users
        if 'user_id' in session and '_csrf_token' not in session:
            session['_csrf_token'] = os.urandom(24).hex()
            
        # Clear expired sessions
        if 'user_id' in session and 'last_activity' in session:
            if time.time() - session['last_activity'] > 3600:  # 1 hour
                session.clear()
                return redirect(url_for('auth_bp.login_page'))
        session['last_activity'] = time.time()

        # Handle public endpoints
        public_endpoints = ['static', 'auth_bp.login', 'auth_bp.login_page']
        if request.endpoint in public_endpoints:
            return

        # Enforce authentication
        if 'user_id' not in session:
            return redirect(url_for('auth_bp.login_page'))

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    # Register blueprints
    app.register_blueprint(home_bp)  # Register home blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(staff_bp, url_prefix='/staff')
    app.register_blueprint(course_bp, url_prefix='/courses')
    app.register_blueprint(class_bp, url_prefix='/classes')
    app.register_blueprint(timetable_bp, url_prefix='/timetable')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/')
    def home():
        user_id = session.get('user_id')
        user = None
        if user_id:
            if isinstance(user_id, str) and '@' in user_id:  # Dummy user
                user = {'email': user_id, 'name': session.get('user_name'), 'role': session.get('user_role')}
            else:
                user = User.query.get(user_id)
        return render_template('index.html', user=user)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('index.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('error.html', error=str(e)), 500

    return app

def init_db(app):
    with app.app_context():
        try:
            db.create_all()
            logging.info("Database tables created successfully")
        except Exception as e:
            logging.error(f"Error creating database tables: {e}")
            raise

if __name__ == "__main__":
    app = create_app()
    init_db(app)
    socketio.run(app, debug=True)
