from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.services.auth import auth_bp
from app.routes.timetable_routes import timetable_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.secret_key = "your_secret_key"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(timetable_bp)

    # Root route
    @app.route("/")
    def home():
        from flask import session, render_template
        from app.models.user_model import User
        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
        return render_template("index.html", user=user)

    with app.app_context():
        db.create_all()

    return app
