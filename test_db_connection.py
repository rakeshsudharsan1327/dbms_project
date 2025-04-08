from app.app import create_app  # Use the correct create_app function
from app.models import db       # Use the shared db instance

app = create_app()

with app.app_context():  # Ensure app context is active
    try:
        connection = db.engine.connect()
        print("Database connection successful!")
        connection.close()
    except Exception as e:
        print(f"Database connection failed: {e}")
