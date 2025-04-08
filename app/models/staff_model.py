from app.models import db
from validate_email import validate_email  # Ensure this is installed

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Remove the misplaced return statement
# Email validation should be handled in the route or service logic
