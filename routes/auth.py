from flask import Blueprint, jsonify, request
from database import db
from flask_jwt_extended import JWTManager, create_access_token
from app import app
from models.user import User

# Set up JWT Manager

auth_routes = Blueprint('auth_routes', __name__, url_prefix='/')

# Initialize JWT Manager
jwt = JWTManager()

# Set the JWT secret key
jwt.init_app(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!




@auth_routes.route('/signup', methods=['POST'])
def signup():
    email = request.json['email']
    password = request.json['password']

    # verify user
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(message='Email already exists'), 409
    
    # create new user
    new_user = User(
        email=email,
        password=password
    )
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