from flask import Blueprint, jsonify, request
from database import db
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from app import app
from models.user import User
from models.patient import Patient
from functools import wraps

# Initialize JWT Manager
jwt = JWTManager()

auth_routes = Blueprint('auth_routes', __name__, url_prefix='/')



# Set the JWT secret key
jwt.init_app(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

# use functools.wraps to preserve the original function name
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

# based on the email of the user, detect if the user is a patient or doctor
def patient_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # get the user identity from the access token
        user_email = get_jwt_identity()
        # get the user object from the database
        user = User.query.filter_by(email=user_email).first()
        # check if the user is an admin
        if user.patient_id:
            return fn(*args, **kwargs)
        return jsonify(message='Patients only!'), 403
    return wrapper

# based on email of user, define a function where data can only be accessed by the related doctor or patient
def doctor_or_patient(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # get the user identity from the access token
        user_email = get_jwt_identity()
        # get the user object from the database
        user = User.query.filter_by(email=user_email).first()
        # check if the user is an admin
        if user.patient_id or user.doctor_id:
            return fn(*args, **kwargs)
        return jsonify(message='Doctors or Patients only!'), 403
    return wrapper



@auth_routes.route('/signup', methods=['POST'])
def signup():
    email = request.json['email']
    password = request.json['password']
    admin = request.json['admin']
    patient_id = request.json['patient_id']
    doctor_id = request.json['doctor_id']

    print(doctor_id,patient_id)

    # verify user
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(message='User already exists!'), 409

    # create new user
    new_user = None
    if patient_id is not None and doctor_id is not None:
        return jsonify(message='Only one of patient_id or doctor_id is allowed!'), 400
    elif patient_id is not None:
        new_user = User(email=email, password=password, admin=admin, patient_id=patient_id)
    elif doctor_id is not None:
        new_user = User(email=email, password=password, admin=admin, doctor_id=doctor_id)

    if new_user is None:
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