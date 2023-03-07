from flask import Blueprint, jsonify, request
from database import db
from models.doctor import Doctor
from schemas.doctor_schema import doctor_schema, doctors_schema

doctor_routes = Blueprint('doctor_routes', __name__, url_prefix='/')

@doctor_routes.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify(doctors_schema.dump(doctors))

@doctor_routes.route('/doctors/<id>', methods=['GET'])
def get_doctor(id):
    doctor = Doctor.query.get(id)
    return jsonify(doctor_schema.dump(doctor))

@doctor_routes.route('/doctors', methods=['POST'])
def add_doctor():
    new_doctor = Doctor(
        first_name=request.json['first_name'],
        last_name=request.json['last_name'],
        email=request.json['email'],
        password=request.json['password'],
        phone_number=request.json['phone_number'],
        AHPRA_number=request.json['AHPRA_number']
    )
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify(doctor_schema.dump(new_doctor))