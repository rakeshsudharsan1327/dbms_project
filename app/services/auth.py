from flask import Blueprint, request, redirect, url_for, session, render_template, jsonify, current_app, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user_model import User
from functools import wraps
from datetime import timedelta
import re
import os
import time

auth_bp = Blueprint('auth_bp', __name__)

# Dummy users (for testing)
def get_dummy_users():
    if current_app.config.get('ENV') != 'development':  # Restrict dummy users
        return {}
    return {
        "admin@example.com": {
            "password": "admin123",
            "role": "admin",
            "name": "Admin User"
        },
        "teacher1@example.com": {
            "password": "teach123",
            "role": "teacher",
            "name": "Prof. John"
        }
    }

# ✅ Login required decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            session.clear()  # Clear any partial session data
            flash('Please login to access this page', 'warning')
            return redirect(url_for('auth_bp.login_page'))
        
        # Refresh session timeout
        session.permanent = True
        session.modified = True
        return f(*args, **kwargs)
    return decorated

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        @login_required  # Ensure user is logged in first
        def decorated(*args, **kwargs):
            user_role = session.get('user_role')
            if not user_role or user_role not in allowed_roles:
                flash('You do not have permission to access this page', 'danger')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated
    return decorator

def password_meets_requirements(password: str) -> bool:
    """Check password strength"""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

# ✅ CSRF Token generation and validation
def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = os.urandom(24).hex()
    return session['_csrf_token']

def validate_csrf_token():
    token = session.get('_csrf_token')
    form_token = request.form.get('_csrf_token') or request.headers.get('X-CSRF-Token')
    return token and form_token and token == form_token

@auth_bp.before_request
def csrf_protect():
    if request.method == "POST":
        if not validate_csrf_token():
            flash('Invalid or missing CSRF token', 'danger')
            return redirect(url_for('auth_bp.login_page'))

# ✅ Login page (GET)
@auth_bp.route('/login', methods=['GET'])
def login_page():
    # Generate CSRF token before rendering the login page
    if '_csrf_token' not in session:
        session['_csrf_token'] = os.urandom(24).hex()
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

# ✅ Login logic (POST) with fallback to dummy_users if DB fails
@auth_bp.route('/login', methods=['POST'])
def login():
    if not validate_csrf_token():
        flash('Invalid or missing CSRF token', 'danger')
        return redirect(url_for('auth_bp.login_page'))

    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Please provide both email and password', 'danger')
        return redirect(url_for('auth_bp.login_page'))

    # Try database user first
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session.clear()
        session['user_id'] = user.user_id
        session['user_role'] = user.role
        session['user_name'] = user.name
        session.permanent = True
        session['last_activity'] = time.time()
        session['_csrf_token'] = generate_csrf_token()
        flash('Successfully logged in!', 'success')
        return redirect(url_for('home'))

    # Fallback to dummy users only in development
    if current_app.config['ENV'] == 'development':
        dummy_users = get_dummy_users()
        dummy = dummy_users.get(email)
        if dummy and dummy['password'] == password:
            session.clear()
            session['user_id'] = email
            session['user_role'] = dummy['role']
            session['user_name'] = dummy['name']
            session.permanent = True
            session['last_activity'] = time.time()
            session['_csrf_token'] = generate_csrf_token()
            flash('Successfully logged in!', 'success')
            return redirect(url_for('home'))

    flash('Invalid email or password', 'danger')
    return redirect(url_for('auth_bp.login_page'))

# ✅ Logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    if not validate_csrf_token():
        flash('Invalid CSRF token', 'danger')
        return redirect(url_for('home'))
    session.clear()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('auth_bp.login_page'))

# ✅ Register (if needed)
@auth_bp.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not all([name, email, password]):
        return 'All fields are required', 400

    if User.query.filter_by(email=email).first():
        return 'Email already exists', 409

    hashed_pw = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth_bp.login_page'))
