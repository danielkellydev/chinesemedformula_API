from flask import Blueprint, jsonify, request
from database import db
from models.patient import Patient
from schemas.patient_schema import patient_schema, patients_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.auth import admin_required, doctor_required, admin_or_doctor_required

patient_routes = Blueprint('patient_routes', __name__, url_prefix='/')

@patient_routes.route('/patients', methods=['GET'])
@jwt_required()
@admin_required
def get_patients():
    patients = Patient.query.all()
    return jsonify(patients_schema.dump(patients))

@patient_routes.route('/patients/<id>', methods=['GET'])
@jwt_required()
@admin_required
def get_patient(id):
    patient = Patient.query.get(id)
    return jsonify(patient_schema.dump(patient))


@patient_routes.route('/patients', methods=['POST'])
@jwt_required()
@admin_or_doctor_required
def add_patient():
    email = request.json['email']
    patient = Patient.query.filter_by(email=email).first()
    if patient:
        return jsonify({'message': 'Email already exists'}), 400
    else:
        new_patient = Patient(
            first_name=request.json['first_name'],
            last_name=request.json['last_name'],
            email=request.json['email'],
            password=request.json['password'],
            phone_number=request.json['phone_number'],
        )
        db.session.add(new_patient)
        db.session.commit()
        return jsonify(patient_schema.dump(new_patient))

@patient_routes.route('/patients/delete/<id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_patient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify(patient_schema.dump(patient))

@patient_routes.route('/patients/update/<id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_patient(id):
    patient = Patient.query.get(id)
    patient.first_name = request.json['first_name']
    patient.last_name = request.json['last_name']
    patient.email = request.json['email']
    patient.password = request.json['password']
    patient.phone_number = request.json['phone_number']
    db.session.commit()
    return jsonify(patient_schema.dump(patient))

