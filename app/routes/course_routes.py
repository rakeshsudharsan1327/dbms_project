from flask import Blueprint, request, jsonify
from app.models.course_model import Courses
from app.models import db  # Fix db import

# Create a Blueprint for course routes
course_bp = Blueprint('course_bp', __name__)

# ✅ Route to get all courses
@course_bp.route('/courses', methods=['GET'])
def get_all_courses():
    courses = Courses.query.all()
    if not courses:
        return jsonify({'message': 'No courses found'}), 404
    
    result = [{
        'course_id': c.course_id,
        'course_code': c.course_code,
        'course_name': c.course_name,
        'classes_per_week': c.classes_per_week,
        'eligible_teachers': c.eligible_teachers
    } for c in courses]
    
    return jsonify(result), 200

# ✅ Route to get a single course by ID
@course_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Courses.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found'}), 404

    return jsonify({
        'course_id': course.course_id,
        'course_code': course.course_code,
        'course_name': course.course_name,
        'classes_per_week': course.classes_per_week,
        'eligible_teachers': course.eligible_teachers
    }), 200

# ✅ Route to add a new course
@course_bp.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    
    # Validate required fields
    if not data or 'course_code' not in data or 'course_name' not in data or 'classes_per_week' not in data:
        return jsonify({'message': 'Course code, name, and classes per week are required'}), 400

    if data['classes_per_week'] <= 0:  # Validate positive integer
        return jsonify({'message': 'Classes per week must be a positive integer'}), 400

    # Check for duplicate course codes
    existing_course = Courses.query.filter_by(course_code=data['course_code']).first()
    if existing_course:
        return jsonify({'message': 'Course code already exists'}), 409

    # Create a new course
    new_course = Courses(
        course_code=data['course_code'],
        course_name=data['course_name'],
        classes_per_week=data['classes_per_week'],
        eligible_teachers=data.get('eligible_teachers', None)  # Optional field
    )

    db.session.add(new_course)
    db.session.commit()
    
    return jsonify({'message': 'Course added successfully', 'course_id': new_course.course_id}), 201

# ✅ Route to update an existing course
@course_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course = Courses.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found'}), 404

    data = request.get_json()
    
    # Update fields only if provided
    course.course_code = data.get('course_code', course.course_code)
    course.course_name = data.get('course_name', course.course_name)
    course.classes_per_week = data.get('classes_per_week', course.classes_per_week)
    course.eligible_teachers = data.get('eligible_teachers', course.eligible_teachers)

    db.session.commit()
    return jsonify({'message': 'Course updated successfully'}), 200

# ✅ Route to delete a course
@course_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Courses.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found'}), 404

    db.session.delete(course)
    db.session.commit()
    
    return jsonify({'message': 'Course deleted successfully'}), 200
