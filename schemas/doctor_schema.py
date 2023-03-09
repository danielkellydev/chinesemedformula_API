from app import ma
from marshmallow import fields

class DoctorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'AHPRA_number')

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)
