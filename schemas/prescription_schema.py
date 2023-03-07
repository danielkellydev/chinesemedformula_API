from app import ma
from marshmallow import fields

class PrescriptionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'formula_id', 'patient_id', 'doctor_id')

prescription_schema = PrescriptionSchema()
prescriptions_schema = PrescriptionSchema(many=True)