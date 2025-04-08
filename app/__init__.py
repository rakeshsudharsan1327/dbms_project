from flask_sqlalchemy import SQLAlchemy

# Initialize the shared db instance
db = SQLAlchemy()

# Import models to ensure they are registered with SQLAlchemy
from app.models.timetable_model import Timetable
from app.models.class_model import Classes
from app.models.course_model import Courses
from app.models.staff_model import Staff
from app.models.user_model import User
