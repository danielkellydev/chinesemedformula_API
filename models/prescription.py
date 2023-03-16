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
    instructions = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'{self.id}'