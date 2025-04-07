from app.models import db

class Timetable(db.Model):
    __tablename__ = 'timetable'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)  # 0=Monday, 5=Saturday
    period = db.Column(db.Integer, nullable=False)  # 0-6 for 7 periods/day
    course_id = db.Column(db.Integer, nullable=False)
    staff_id = db.Column(db.Integer, nullable=False)
