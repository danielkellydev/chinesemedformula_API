from flask import Blueprint, jsonify
from models.user import User
from schemas.user_schema import users_schema, user_schema
from flask_jwt_extended import jwt_required
from routes.auth import admin_required
from database import db


user_routes = Blueprint('user_routes', __name__, url_prefix='/')

@user_routes.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@user_routes.route('/users/<id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))