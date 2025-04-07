from flask import Blueprint, request, redirect, url_for, session, render_template, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import db, User
from functools import wraps

auth_bp = Blueprint('auth_bp', __name__)

# Dummy users (for testing)
dummy_users = {
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
            return redirect(url_for('auth_bp.login_page'))
        return f(*args, **kwargs)
    return decorated

# ✅ Login page (GET)
@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')  # make sure templates/login.html exists

# ✅ Login logic (POST) with fallback to dummy_users if DB fails
@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.user_id
        session['user_role'] = 'db_user'
        return redirect(url_for('home'))

    # Fallback to dummy users
    dummy = dummy_users.get(email)
    if dummy and dummy['password'] == password:
        session['user_id'] = email  # Just using email as ID for dummy
        session['user_role'] = dummy['role']
        session['user_name'] = dummy['name']
        return redirect(url_for('home'))

    return 'Login failed', 401

# ✅ Logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('user_role', None)
    session.pop('user_name', None)
    return redirect(url_for('home'))

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
