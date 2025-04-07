from flask import Flask, send_from_directory, jsonify, render_template, session
from app.config import Config
from app.models import db
from app.routes.staff_routes import staff_bp
from app.routes.course_routes import course_bp
from app.routes.class_routes import class_bp
from app.routes.timetable_routes import timetable_bp
from app.services.auth import auth_bp
from flask_socketio import SocketIO
from app.models.user_model import User
from app.swagger import swaggerui_blueprint, SWAGGER_URL
from dotenv import load_dotenv
from flask_cors import CORS
import logging
import os

socketio = SocketIO()

def create_app():
    app = Flask(__name__, template_folder='templates')
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

    @app.route('/')
    def home():
        user_id = session.get('user_id')
        if user_id:
            user = db.session.get(User, user_id)
        else:
            user = None
        return render_template('index.html', user=user)


    # Inject logged-in user into all Jinja templates
    @app.context_processor
    def inject_user():
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            return dict(user=user)
        return dict(user=None)

    @app.route('/static/swagger.json')
    def serve_swagger():
        return send_from_directory('static', 'swagger.json')

    @app.errorhandler(404)
    def frontend_404(e):
        return render_template('index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    if app.config.get('ENV', 'development') == 'development':
        with app.app_context():
            db.create_all()
    socketio.run(app, debug=True)
