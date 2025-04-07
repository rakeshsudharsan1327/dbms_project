from flask import jsonify
from app.models.timetable_model import db, Timetable
from app.models.course_model import Courses
from app.models.class_model import Classes
from app.models.staff_model import Staff

# Function to generate a timetable

def generate_timetable():
    try:
        classes = Classes.query.all()
        courses = Courses.query.all()
        staff = Staff.query.all()
        
        # Clear existing timetable
        db.session.query(Timetable).delete()
        db.session.commit()

        # Sample logic for scheduling (simple round-robin)
        for cls in classes:
            period = 1
            for course in courses:
                eligible_staff = [s for s in staff if s.staff_id == course.eligible_teachers]
                if not eligible_staff:
                    continue
                
                timetable_entry = Timetable(
                    class_id=cls.class_id,
                    day='Monday',  # Placeholder, should be dynamically assigned
                    period=period,
                    course_id=course.course_id,
                    staff_id=eligible_staff[0].staff_id
                )
                db.session.add(timetable_entry)
                period += 1
                if period > 7:  # Assuming 7 periods per day
                    break
        
        db.session.commit()
        return jsonify({'message': 'Timetable generated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500