from flask import Blueprint, render_template, session
from app.models import User

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def index():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    return render_template('index.html', user=user)
