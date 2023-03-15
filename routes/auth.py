from flask import Blueprint, jsonify, request
from database import db
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from app import app
from models.user import User
from models.doctor import Doctor
from models.patient import Patient
from models.prescription import Prescription
from functools import wraps

# Initialize JWT Manager
jwt = JWTManager()

auth_routes = Blueprint('auth_routes', __name__, url_prefix='/')



# Set the JWT secret key
jwt.init_app(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

# WRAPS
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # get the user identity from the access token
        user_email = get_jwt_identity()
        # get the user object from the database
        user = User.query.filter_by(email=user_email).first()
        # check if the user is an admin
        if not user.admin:
            return jsonify(message='Admins only!'), 403
        # otherwise continue with the original route function
        return fn(*args, **kwargs)
    return wrapper


def doctor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # get the user identity from the access token
        user_email = get_jwt_identity()
        # get the user object from the database
        user = User.query.filter_by(email=user_email).first()
        # check if the user is an admin
        if not user.doctor_id:
            return jsonify(message='Doctors only!'), 403
        # otherwise continue with the original route function
        return fn(*args, **kwargs)
    return wrapper


def admin_or_doctor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # get the user identity from the access token
        user_email = get_jwt_identity()
        # get the user object from the database
        user = User.query.filter_by(email=user_email).first()
        # check if the user is an admin or doctor
        if not user.admin and not user.doctor_id:
            return jsonify(message='Admins or doctors only!'), 403
        # otherwise continue with the original route function
        return fn(*args, **kwargs)
    return wrapper
# This wrapper is not working, patients can access the route. I need to re-write it.



# based on the email of the user, detect if the user is a patient or doctor
def patient_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_email = get_jwt_identity()
        if 'email' in kwargs and kwargs['email'] != current_user_email:
            return jsonify(message='Unauthorized access'), 401
        return f(*args, **kwargs)
    return decorated_function

def doctor_or_admin_only():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_email = get_jwt_identity()
            if 'email' in kwargs and kwargs['email'] != current_user_email:
                return jsonify(message='Unauthorized access'), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# decorator to use so that only an admin or the doctor who created the prescription can access it.
def requires_prescription_access(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        prescription_id = kwargs.get('id')
        prescription = Prescription.query.get(prescription_id)
        if prescription is None:
            return jsonify({'message': 'Prescription not found.'}), 404

        current_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=current_user_email).first()

        if current_user is None:
            return jsonify({'message': 'Unauthorized access.'}), 401

        if current_user.doctor_id == prescription.doctor_id or current_user.admin:
            return route_function(*args, **kwargs)

        return jsonify({'message': 'Unauthorized access.'}), 401

    return wrapper

# ROUTES

@auth_routes.route('/signup', methods=['POST'])
def signup():
    email = request.json['email']
    password = request.json['password']
    admin = request.json['admin']
    patient_id = request.json['patient_id']
    doctor_id = request.json['doctor_id']

    print(doctor_id, patient_id)

    # verify user
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(message='User already exists!'), 409

# check patient_id and doctor_id
    if patient_id is not None:
        patient = Patient.query.get(patient_id)
        if patient is None:
            return jsonify(message=f'Patient with id {patient_id} not found!'), 404
    if doctor_id is not None:
        doctor = Doctor.query.get(doctor_id)
        if doctor is None:
            return jsonify(message=f'Doctor with id {doctor_id} not found!'), 404

    # create new user
    if admin:
        patient_id = None
        doctor_id = None

    new_user = User(email=email, password=password, admin=admin, patient_id=patient_id, doctor_id=doctor_id)

    if (not admin) and (patient_id is None) and (doctor_id is None):
        return jsonify(message='Either patient_id or doctor_id is required!'), 400

    
    db.session.add(new_user)
    db.session.commit()
    # create access token
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

    



@auth_routes.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password'] 

    # verify user
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify(message='Bad email or password'), 401
    
    # create access token

    access_token = create_access_token(identity=email)

    return jsonify(access_token=access_token)