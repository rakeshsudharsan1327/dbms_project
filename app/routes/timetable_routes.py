from flask import Blueprint, request, jsonify
from app.models import db
from app.models.timetable_model import Timetable

# ✅ Declare the blueprint
timetable_bp = Blueprint('timetable_bp', __name__)

# ✅ Sample route to generate timetable
@timetable_bp.route('/generate', methods=['POST'])
def generate_timetable():
    # Placeholder logic for now
    return jsonify({"message": "Timetable generation route reached."})

# ✅ Route to get timetable for a class
@timetable_bp.route('/view/<int:class_id>', methods=['GET'])
def get_timetable(class_id):
    timetable = Timetable.query.filter_by(class_id=class_id).all()
    if not timetable:
        return jsonify({"error": "No timetable found for this class."}), 404

    return jsonify([t.to_dict() for t in timetable])



"""from flask import Flask, send_from_directory
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
"""