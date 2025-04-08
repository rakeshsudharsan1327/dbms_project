from flask import Blueprint, request, jsonify
from app.models.class_model import Classes
from app.models import db  # Fix db import

# Create a Blueprint for class routes
class_bp = Blueprint('class_bp', __name__)

# ✅ Route to get all classes
@class_bp.route('/classes', methods=['GET'])
def get_all_classes():
    classes = Classes.query.all()
    if not classes:
        return jsonify({'message': 'No classes found'}), 404
    
    result = [{
        'class_id': c.class_id,
        'class_name': c.class_name,
        'degree': c.degree,
        'semester': c.semester,
        'batch_number': c.batch_number
    } for c in classes]

    return jsonify(result), 200

# ✅ Route to get a single class by ID
@class_bp.route('/classes/<int:class_id>', methods=['GET'])
def get_class(class_id):
    cls = Classes.query.get(class_id)
    if not cls:
        return jsonify({'message': 'Class not found'}), 404

    return jsonify({
        'class_id': cls.class_id,
        'class_name': cls.class_name,
        'degree': cls.degree,
        'semester': cls.semester,
        'batch_number': cls.batch_number
    }), 200

# ✅ Route to add a new class
@class_bp.route('/classes', methods=['POST'])
def add_class():
    data = request.get_json()

    # Validate required fields
    required_fields = ['class_name', 'degree', 'semester', 'batch_number']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'All fields (class_name, degree, semester, batch_number) are required'}), 400

    if data['semester'] <= 0:  # Validate positive integer
        return jsonify({'message': 'Semester must be a positive integer'}), 400

    # Check for duplicate class entries
    existing_class = Classes.query.filter_by(class_name=data['class_name'], degree=data['degree'], semester=data['semester']).first()
    if existing_class:
        return jsonify({'message': 'Class with the same name, degree, and semester already exists'}), 409

    # Create new class record
    new_class = Classes(
        class_name=data['class_name'],
        degree=data['degree'],
        semester=data['semester'],
        batch_number=data['batch_number']
    )

    db.session.add(new_class)
    db.session.commit()

    return jsonify({'message': 'Class added successfully', 'class_id': new_class.class_id}), 201

# ✅ Route to update an existing class
@class_bp.route('/classes/<int:class_id>', methods=['PUT'])
def update_class(class_id):
    cls = Classes.query.get(class_id)
    if not cls:
        return jsonify({'message': 'Class not found'}), 404

    data = request.get_json()

    # Update fields only if provided
    cls.class_name = data.get('class_name', cls.class_name)
    cls.degree = data.get('degree', cls.degree)
    cls.semester = data.get('semester', cls.semester)
    cls.batch_number = data.get('batch_number', cls.batch_number)

    db.session.commit()
    return jsonify({'message': 'Class updated successfully'}), 200

# ✅ Route to delete a class
@class_bp.route('/classes/<int:class_id>', methods=['DELETE'])
def delete_class(class_id):
    cls = Classes.query.get(class_id)
    if not cls:
        return jsonify({'message': 'Class not found'}), 404

    db.session.delete(cls)
    db.session.commit()

    return jsonify({'message': 'Class deleted successfully'}), 200
