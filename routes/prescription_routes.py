from flask import Blueprint, jsonify, request
from database import db
from models.prescription import Prescription
from models.patient import Patient
from models.doctor import Doctor
from models.formula import Formula
from schemas.prescription_schema import prescription_schema, prescriptions_schema
from flask_jwt_extended import jwt_required, current_user
from routes.auth import jwt
from routes.auth import doctor_required, patient_only, admin_required, doctor_or_admin_only, requires_prescription_access


prescription_routes = Blueprint('prescription_routes', __name__, url_prefix='/')

# Get all prescriptions, must be admin
@prescription_routes.route('/prescriptions', methods=['GET'])
@jwt_required()
@admin_required
def get_prescriptions():
    prescriptions = Prescription.query.all()
    return jsonify(prescriptions_schema.dump(prescriptions))

# Get prescription by id, must be admin or prescribing doctor
@prescription_routes.route('/prescriptions/<id>', methods=['GET'])
@jwt_required()
@requires_prescription_access
def get_prescription(id):
    prescription = Prescription.query.get(id)
    return jsonify(prescription_schema.dump(prescription))

# Add prescription, must be doctor
@prescription_routes.route('/prescriptions', methods=['POST'])
@jwt_required()
@doctor_required
def add_prescription():
    try:
        patient_id = request.json['patient_id']
        formula_id = request.json['formula_id']
        doctor_id = request.json['doctor_id']
    except KeyError as e:
        return jsonify({'message': f'Missing {e.args[0]} field'}), 400
    
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'message': f'Patient with id {patient_id} not found'}), 404
    
    formula = Formula.query.get(formula_id)
    if not formula:
        return jsonify({'message': f'Formula with id {formula_id} not found'}), 404
    
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'message': f'Doctor with id {doctor_id} not found'}), 404

    new_prescription = Prescription(
        patient_id=patient_id,
        formula_id=formula_id,
        doctor_id=doctor_id,
        instructions=request.json['instructions']
    )
    db.session.add(new_prescription)
    db.session.commit()
    return jsonify(prescription_schema.dump(new_prescription))


# Get prescriptions by patient id, must be admin or prescribing doctor
@prescription_routes.route('/prescriptions/patient/<patient_id>', methods=['GET'])
@jwt_required()
@requires_prescription_access
def get_patient_prescriptions(patient_id):
    prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
    return jsonify(prescriptions_schema.dump(prescriptions))

# Get prescriptions by doctor id, must be admin or prescribing doctor
@prescription_routes.route('/prescriptions/doctor/<doctor_id>', methods=['GET'])
@jwt_required()
@requires_prescription_access
def get_doctor_prescriptions(doctor_id):
    prescriptions = Prescription.query.filter_by(doctor_id=doctor_id).all()
    return jsonify(prescriptions_schema.dump(prescriptions))

# Get prescriptions by patient id and doctor id, must be admin or prescribing doctor
@prescription_routes.route('/prescriptions/patient/<patient_id>/doctor/<doctor_id>', methods=['GET'])
@jwt_required()
@requires_prescription_access
def get_patient_doctor_prescriptions(patient_id, doctor_id):
    prescriptions = Prescription.query.filter_by(patient_id=patient_id, doctor_id=doctor_id).all()
    return jsonify(prescriptions_schema.dump(prescriptions))

# Get prescriptions by email. For email entered, reference patient table to get patient id, then query prescriptions by patient id.
# Main endpoint for patient to view their prescriptions
@prescription_routes.route('/prescriptions/patient/email/<email>', methods=['GET'])
@jwt_required()
@patient_only
def get_patient_prescriptions_by_email(email):
    patient = Patient.query.filter_by(email=email).first()
    if not patient:
        return jsonify(message='Patient not found'), 404
    prescriptions = Prescription.query.filter_by(patient_id=patient.id).all()
    return jsonify(prescriptions_schema.dump(prescriptions))

# Update prescriptions by id, must be admin or prescribing doctor
@prescription_routes.route('/prescriptions/update/<id>', methods=['PUT'])
@jwt_required()
@requires_prescription_access
def update_prescription(id):
    prescription = Prescription.query.get(id)
    prescription.patient_id = request.json['patient_id']
    prescription.formula_id = request.json['formula_id']
    prescription.doctor_id = request.json['doctor_id']
    prescription.instructions = request.json['instructions']
    db.session.commit()
    return jsonify(prescription_schema.dump(prescription))

# Delete prescriptions by id, must be admin
@prescription_routes.route('/prescriptions/delete/<id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_prescription(id):
    prescription = Prescription.query.get(id)
    db.session.delete(prescription)
    db.session.commit()
    return jsonify(prescription_schema.dump(prescription))