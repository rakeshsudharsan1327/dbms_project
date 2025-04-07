from app.models import db

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
