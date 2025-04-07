from flask import Flask, jsonify, request
from app.models import db, Timetable
from app.models.class_model import Classes
from app.models.course_model import Courses
from app.models.staff_model import Staff

import random

app = Flask(__name__)

# 💾 Database configuration
app.config.from_object('app.config.Config')  # Use centralized config

# 🔌 Initialize SQLAlchemy
db.init_app(app)

@app.route('/generate-timetable', methods=['POST'])
def generate_timetable_api():
    try:
        generate_timetable()
        return jsonify({'message': 'Timetable generated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_timetable():
    print("Fetching all classes...")
    classes = Classes.query.all()
    print(f"Found {len(classes)} classes.")
    print("Fetching all courses...")
    courses = Courses.query.all()
    print(f"Found {len(courses)} courses.")
    print("Fetching all staff...")
    staff = Staff.query.all()
    print(f"Found {len(staff)} staff members.")
    print("Clearing existing timetable...")
    db.session.query(Timetable).delete()

    print("Generating timetable...")
    for cls in classes:
        print(f"Generating timetable for class {cls.class_id}...")
        for day in range(5):  # Monday to Friday
            for period in range(7):  # 7 periods per day
                course = random.choice(courses)
                eligible_teachers = course.eligible_teachers.split(',')
                teacher_id = random.choice(eligible_teachers)
                timetable_entry = Timetable(
                    class_id=cls.class_id,
                    day=day,
                    period=period,
                    course_id=course.course_id,
                    staff_id=teacher_id
                )
                db.session.add(timetable_entry)
    db.session.commit()
    print("Timetable generation completed.")
@app.route("/")
def home():
    return send_from_directory('../frontend', 'index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
