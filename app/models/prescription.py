from app.routes import db

# create a prescription model
class Prescription(db.Model):
    __tablename__ = 'prescriptions'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80), nullable=False)
    formula_id = db.Column(db.Integer, db.ForeignKey('formulas.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)