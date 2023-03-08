from app import db
from models.patient import Patient
from models.doctor import Doctor
from models.formula import Formula
from sqlalchemy import ForeignKey
from datetime import datetime

# create a prescription model
class Prescription(db.Model):
    __tablename__ = 'prescriptions'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    formula_id = db.Column(db.Integer, db.ForeignKey('formulas.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    # code to return a string when a new prescription is created
    def generate_prescription_data(self):
        formula = Formula.query.filter_by(id=self.formula_id).first()
        patient = Patient.query.filter_by(id=self.patient_id).first()
        doctor = Doctor.query.filter_by(id=self.doctor_id).first()

        prescription_data = f"{formula.name} for {patient.first_name} {patient.last_name} (DOB: {patient.dob}), prescribed by Dr. {doctor.first_name} {doctor.last_name} (AHPRA number: {doctor.AHPRA_number}) on {self.date}"

        return prescription_data