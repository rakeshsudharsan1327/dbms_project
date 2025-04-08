from app.models import db  # Import the shared db instance

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user', server_default='user')

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"
