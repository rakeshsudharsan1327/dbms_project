from app.models import db

class Courses(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    classes_per_week = db.Column(db.Integer, nullable=False)
    is_lab = db.Column(db.Boolean, default=False)
    
    # Define relationships
    staff = db.relationship('Staff', secondary='course_staff', backref='courses')

class CourseStaff(db.Model):
    __tablename__ = 'course_staff'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id', ondelete='CASCADE'), nullable=False)