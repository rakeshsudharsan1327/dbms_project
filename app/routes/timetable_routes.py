from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, session
from app.services.timetable_generator import TimetableGenerator
from app.services.auth import login_required, role_required, validate_csrf_token
from app.models import db
from app.models.timetable_model import Timetable
from app.models.course_model import Courses
from app.models.staff_model import Staff

timetable_bp = Blueprint('timetable_bp', __name__)

@timetable_bp.route('/generate', methods=['POST'])
@login_required
@role_required(['admin'])
def generate_timetable():
    """Generate a new timetable (admin only)"""
    if not validate_csrf_token():
        flash('Invalid or missing CSRF token', 'danger')
        return redirect(url_for('home'))

    if session.get('user_role') != 'admin':
        flash('Only administrators can generate timetables', 'danger')
        return redirect(url_for('home'))

    try:
        generator = TimetableGenerator()
        success, message = generator.generate()
        
        if success:
            flash('Timetable generated successfully', 'success')
            return jsonify({"message": message}), 200
        return jsonify({"error": message}), 500
    except Exception as e:
        flash(f'Error generating timetable: {str(e)}', 'danger')
        return jsonify({"error": str(e)}), 500

@timetable_bp.route('/view/<int:class_id>')
@login_required
def view_timetable(class_id):
    """View timetable for a specific class"""
    try:
        user_role = session.get('user_role')
        user_id = session.get('user_id')
        
        if not user_role or not user_id:
            flash('Please login again', 'warning')
            return redirect(url_for('auth_bp.login_page'))

        # Admin can view all timetables
        if user_role == 'admin':
            pass  # Allow access
        # Teachers can only view their assigned classes
        elif user_role == 'teacher':
            if isinstance(user_id, str):  # Dummy teacher
                pass  # Allow for demo
            else:
                teacher_classes = Timetable.query.filter_by(staff_id=user_id).all()
                if not any(t.class_id == class_id for t in teacher_classes):
                    flash('You can only view timetables for classes you teach', 'warning')
                    return redirect(url_for('home'))
        else:
            flash('Unauthorized access', 'danger')
            return redirect(url_for('home'))

        # Rest of the view_timetable code...
        timetable = Timetable.query.filter_by(class_id=class_id).all()
        if not timetable:
            flash('No timetable found for this class', 'warning')
            return redirect(url_for('home'))

        # Format timetable data
        timetable_grid = [[None for _ in range(7)] for _ in range(5)]
        for entry in timetable:
            course = Courses.query.get(entry.course_id)
            staff = Staff.query.get(entry.staff_id)
            timetable_grid[entry.day][entry.period] = {
                'course_name': course.course_name if course else 'Unknown Course',
                'staff_name': staff.name if staff else 'Unknown Staff',
                'room': getattr(entry, 'room', 'TBD'),
                'is_lab': getattr(entry, 'is_lab', False)
            }

        return render_template(
            'timetable_view.html',
            timetable=timetable_grid,
            class_id=class_id,
            is_break_period=lambda p: (class_id == 1 and p == 2) or (class_id != 1 and p == 3),
            is_lunch_period=lambda p: (class_id == 1 and p == 4) or (class_id != 1 and p == 5),
            is_academic_slot=lambda d, p: d == 2 and p >= 4  # Wednesday afternoon
        )

    except Exception as e:
        flash(f'Error viewing timetable: {str(e)}', 'danger')
        return redirect(url_for('home'))



from flask import Flask, send_from_directory
from app.config import Config  # Import configuration settings
from app.models import db  # Import shared db instance
from app.routes.staff_routes import staff_bp
from app.routes.course_routes import course_bp
from app.routes.class_routes import class_bp # ✅ No circular import
from app.services.auth import auth_bp
from flask_socketio import SocketIO
from app.swagger import swaggerui_blueprint, SWAGGER_URL
from dotenv import load_dotenv
import os
from flask_cors import CORS
import logging

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    load_dotenv()

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(staff_bp, url_prefix='/staff')
    app.register_blueprint(course_bp, url_prefix='/courses')
    app.register_blueprint(class_bp, url_prefix='/classes')
    app.register_blueprint(timetable_bp, url_prefix='/timetable')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    socketio.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route("/")
    def home():
        return send_from_directory('../frontend', 'index.html')

    @app.route('/<path:path>')
    def serve_frontend(path):
        return send_from_directory('../frontend', path)

    @app.route('/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory('../frontend/js', filename)

    @app.route('/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory('../frontend/css', filename)

    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        return send_from_directory('../frontend/assets', filename)

    @app.route('/static/swagger.json')
    def serve_swagger():
        return send_from_directory('static', 'swagger.json')

    @app.errorhandler(404)
    def frontend_404(e):
        return send_from_directory('../frontend', 'index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    if app.config['ENV'] == 'development':
        with app.app_context():
            db.create_all()  # Create tables if they don't exist
    socketio.run(app, debug=True)