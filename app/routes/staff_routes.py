from flask import Blueprint, request, jsonify
from app.models import db
from app.models.staff_model import Staff

# Create a Blueprint for staff routes
staff_bp = Blueprint('staff_bp', __name__)

# ✅ Route to get all staff members
@staff_bp.route('/staff', methods=['GET'])
def get_all_staff():
    staff_list = Staff.query.all()  # Fetch all staff records
    if not staff_list:
        return jsonify({'message': 'No staff members found'}), 404
    
    result = [{'staff_id': s.staff_id, 'name': s.name, 'email': s.email} for s in staff_list]
    return jsonify(result), 200

# ✅ Route to get a single staff member by ID
@staff_bp.route('/staff/<int:staff_id>', methods=['GET'])
def get_staff(staff_id):
    staff = Staff.query.get(staff_id)  # Fetch staff by ID
    if not staff:
        return jsonify({'message': 'Staff member not found'}), 404

    return jsonify({'staff_id': staff.staff_id, 'name': staff.name, 'email': staff.email}), 200

# ✅ Route to add a new staff member
@staff_bp.route('/staff', methods=['POST'])
def add_staff():
    data = request.get_json()
    
    # Check if required fields are provided
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'message': 'Name and Email are required'}), 400

    # Check if the email already exists
    existing_staff = Staff.query.filter_by(email=data['email']).first()
    if existing_staff:
        return jsonify({'message': 'Email already exists'}), 409
    
    # Create new staff record
    new_staff = Staff(name=data['name'], email=data['email'])
    db.session.add(new_staff)
    db.session.commit()

    return jsonify({'message': 'Staff member added successfully', 'staff_id': new_staff.staff_id}), 201

# ✅ Route to update an existing staff member
@staff_bp.route('/staff/<int:staff_id>', methods=['PUT'])
def update_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        return jsonify({'message': 'Staff member not found'}), 404

    data = request.get_json()
    
    staff.name = data.get('name', staff.name)
    staff.email = data.get('email', staff.email)
    
    db.session.commit()
    return jsonify({'message': 'Staff member updated successfully'}), 200

# ✅ Route to delete a staff member
@staff_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        return jsonify({'message': 'Staff member not found'}), 404

    db.session.delete(staff)
    db.session.commit()
    return jsonify({'message': 'Staff member deleted successfully'}), 200
