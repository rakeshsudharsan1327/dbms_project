from app.extensions import db

# Import models
from app.models.user_model import User
from app.models.staff_model import Staff
from app.models.course_model import Courses, CourseStaff
from app.models.class_model import Classes
from app.models.timetable_model import Timetable

# Export models
__all__ = ['db', 'User', 'Staff', 'Courses', 'CourseStaff', 'Classes', 'Timetable']