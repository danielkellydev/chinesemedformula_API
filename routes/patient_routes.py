from flask import Blueprint, jsonify, request
from database import db
from models.patient import Patient
from schemas.patient_schema import patient_schema, patients_schema

patient_routes = Blueprint('patient_routes', __name__, url_prefix='/')

@patient_routes.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify(patients_schema.dump(patients))

@patient_routes.route('/patients/<id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.get(id)
    return jsonify(patient_schema.dump(patient))

@patient_routes.route('/patients', methods=['POST'])
def add_patient():
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

