from app import ma
from marshmallow import fields

class PatientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'doctor_id', "formula_id")

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)