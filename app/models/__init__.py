from flask_sqlalchemy import SQLAlchemy

# Create a single SQLAlchemy instance
db = SQLAlchemy()

# Import all models here
from app.models.timetable_model import Timetable
from app.models.class_model import Classes
from app.models.course_model import Courses
from app.models.staff_model import Staff
from app.models.user_model import User