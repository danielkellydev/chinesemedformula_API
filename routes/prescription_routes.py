from flask import Blueprint, jsonify, request
from database import db
from models.prescription import Prescription
from schemas.prescription_schema import prescription_schema, prescriptions_schema
from flask_jwt_extended import jwt_required
from routes.auth import jwt
from routes.auth import admin_required


prescription_routes = Blueprint('prescription_routes', __name__, url_prefix='/')


@prescription_routes.route('/prescriptions', methods=['GET'])
@jwt_required()
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
@admin_required
def add_prescription():
    new_prescription = Prescription(
        patient_id=request.json['patient_id'],
        formula_id=request.json['formula_id'],
        doctor_id=request.json['doctor_id']
    )
    db.session.add(new_prescription)
    db.session.commit()
    return jsonify(prescription_schema.dump(new_prescription))