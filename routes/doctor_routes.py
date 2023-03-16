from flask import Blueprint, jsonify, request
from database import db
from models.doctor import Doctor
from schemas.doctor_schema import doctor_schema, doctors_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.auth import admin_required

doctor_routes = Blueprint('doctor_routes', __name__, url_prefix='/')

# Get all doctors, must be admin
@doctor_routes.route('/doctors', methods=['GET'])
@jwt_required()
@admin_required
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify(doctors_schema.dump(doctors))

# Get a doctor by id, must be admin
@doctor_routes.route('/doctors/<id>', methods=['GET'])
@jwt_required()
@admin_required
def get_doctor(id):
    doctor = Doctor.query.get(id)
    return jsonify(doctor_schema.dump(doctor))

# Add a doctor, must be admin
@doctor_routes.route('/doctors', methods=['POST'])
@jwt_required()
@admin_required
def add_doctor():
    new_doctor = Doctor(
        first_name=request.json['first_name'],
        last_name=request.json['last_name'],
        email=request.json['email'],
        phone_number=request.json['phone_number'],
        AHPRA_number=request.json['AHPRA_number'],
    )
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify(doctor_schema.dump(new_doctor))

# Delete a doctor, must be admin
@doctor_routes.route('/doctors/delete/<id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    db.session.delete(doctor)
    db.session.commit()
    return jsonify(doctor_schema.dump(doctor))

# Update a doctor, must be admin
@doctor_routes.route('/doctors/update/<id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_doctor(id):
    doctor = Doctor.query.get(id)
    doctor.first_name = request.json['first_name']
    doctor.last_name = request.json['last_name']
    doctor.email = request.json['email']
    doctor.phone_number = request.json['phone_number']
    doctor.AHPRA_number = request.json['AHPRA_number']
    db.session.commit()
    return jsonify(doctor_schema.dump(doctor))