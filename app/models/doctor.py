from app.routes import db
from app.models.patient import Patient

# create a doctor model
class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(120), nullable=False)
    AHPRA_number = db.Column(db.String(120), nullable=False)
    patients = db.relationship('Patient', backref='doctor', lazy=True)

    def __repr__(self):
        return f'{self.name}'