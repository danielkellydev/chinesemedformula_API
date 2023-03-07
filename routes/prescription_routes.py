from flask import Blueprint, jsonify, request
from database import db
from models.prescription import Prescription
from schemas.prescription_schema import prescription_schema, prescriptions_schema


prescription_routes = Blueprint('prescription_routes', __name__, url_prefix='/')


@prescription_routes.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    prescriptions = Prescription.query.all()
    return jsonify(prescriptions_schema.dump(prescriptions))


@prescription_routes.route('/prescriptions/<id>', methods=['GET'])
def get_prescription(id):
    prescription = Prescription.query.get(id)
    return jsonify(prescription_schema.dump(prescription))