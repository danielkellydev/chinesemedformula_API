from flask import Blueprint, jsonify, request
from database import db
from models.prescription import Prescription
from models.patient import Patient
from schemas.prescription_schema import prescription_schema, prescriptions_schema
from flask_jwt_extended import jwt_required, current_user
from routes.auth import jwt
from routes.auth import doctor_required, patient_only, admin_required


prescription_routes = Blueprint('prescription_routes', __name__, url_prefix='/')


@prescription_routes.route('/prescriptions', methods=['GET'])
@jwt_required()
@admin_required
def get_prescriptions():
    prescriptions = Prescription.query.all()
    return jsonify(prescriptions_schema.dump(prescriptions))


@prescription_routes.route('/prescriptions/<id>', methods=['GET'])
@jwt_required()
def get_prescription(id):
    prescription = Prescription.query.get(id)
    return jsonify(prescription_schema.dump(prescription))

@prescription_routes.route('/prescriptions', methods=['POST'])
@jwt_required()
@doctor_required
def add_prescription():
    new_prescription = Prescription(
        patient_id=request.json['patient_id'],
        formula_id=request.json['formula_id'],
        doctor_id=request.json['doctor_id']
    )
    db.session.add(new_prescription)
    db.session.commit()
    return jsonify(prescription_schema.dump(new_prescription))


# query prescriptions by patient id
@prescription_routes.route('/prescriptions/patient/<patient_id>', methods=['GET'])
@jwt_required()
@doctor_required
def get_patient_prescriptions(patient_id):
    prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
    return jsonify(prescriptions_schema.dump(prescriptions))

# query prescriptions by doctor id
@prescription_routes.route('/prescriptions/doctor/<doctor_id>', methods=['GET'])
@jwt_required()
@doctor_required
def get_doctor_prescriptions(doctor_id):
    prescriptions = Prescription.query.filter_by(doctor_id=doctor_id).all()
    return jsonify(prescriptions_schema.dump(prescriptions))

# query prescriptions by patient id and doctor id
@prescription_routes.route('/prescriptions/patient/<patient_id>/doctor/<doctor_id>', methods=['GET'])
@jwt_required()
@doctor_required
def get_patient_doctor_prescriptions(patient_id, doctor_id):
    prescriptions = Prescription.query.filter_by(patient_id=patient_id, doctor_id=doctor_id).all()
    return jsonify(prescriptions_schema.dump(prescriptions))

#  query by email. For email entered, reference patient table to get patient id, then query prescriptions by patient id
@prescription_routes.route('/prescriptions/patient/email/<email>', methods=['GET'])
@jwt_required()
@patient_only
def get_patient_prescriptions_by_email(email):
    patient = Patient.query.filter_by(email=email).first()
    if not patient:
        return jsonify(message='Patient not found'), 404
    prescriptions = Prescription.query.filter_by(patient_id=patient.id).all()
    return jsonify(prescriptions_schema.dump(prescriptions))

# Delete prescriptions by id
@prescription_routes.route('/prescriptions/delete/<id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_prescription(id):
    prescription = Prescription.query.get(id)
    db.session.delete(prescription)
    db.session.commit()
    return jsonify(prescription_schema.dump(prescription))