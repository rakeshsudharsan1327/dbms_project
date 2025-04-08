from flask import Flask, jsonify, request, send_from_directory
from app.extensions import db  # Fix db import
from app.models.timetable_model import Timetable
from app.models.class_model import Classes
from app.models.course_model import Courses
from app.models.staff_model import Staff
from app.services.timetable_service import timetable_service

app = Flask(__name__)

# 💾 Database configuration
app.config.from_object('app.config.Config')  # Use centralized config

# 🔌 Initialize SQLAlchemy
db.init_app(app)

# Register Blueprints
app.register_blueprint(timetable_service)

@app.route("/")
def home():
    return send_from_directory('../frontend', 'index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
