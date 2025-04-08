from app.models import db  # Use the shared db instance

class Classes(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    batch_number = db.Column(db.String(10), nullable=False)
    default_room = db.Column(db.String(50), nullable=True)  # Ensure optional