from app.models import db

class Courses(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    classes_per_week = db.Column(db.Integer, nullable=False)
    eligible_teachers = db.Column(db.String(255), nullable=True)  # Comma-separated list of teacher IDs