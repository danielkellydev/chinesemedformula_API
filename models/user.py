from werkzeug.security import generate_password_hash, check_password_hash
from database import db

class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=True, unique=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True, unique=True)

    def __init__(self, email, password, admin=False, patient_id=None, doctor_id=None):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.admin = admin
        self.patient_id = patient_id
        self.doctor_id = doctor_id

        # Set patient_id and doctor_id to None if both are not provided
        if self.patient_id is None and self.doctor_id is None:
            self.patient_id = None
            self.doctor_id = None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)