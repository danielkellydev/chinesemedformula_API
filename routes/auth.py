from flask import Blueprint, jsonify, request
from database import db
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from app import app
from models.user import User
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


@auth_routes.route('/signup', methods=['POST'])
def signup():
    email = request.json['email']
    password = request.json['password']
    admin = request.json['admin']

    # verify user
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(message='User already exists!'), 409

    # create new user
    new_user = User(email=email, password=password, admin=admin)
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