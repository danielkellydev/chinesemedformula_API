from flask import Blueprint, jsonify, request
from database import db
from models.formula import Formula
from schemas.formula_schema import formula_schema, formulas_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.auth import admin_required, doctor_required

formula_routes = Blueprint('formula_routes', __name__, url_prefix='/')

@formula_routes.route('/formulas', methods=['GET'])
@jwt_required()
@doctor_required
def get_formulas():
    formulas = Formula.query.all()
    return jsonify(formulas_schema.dump(formulas))

@formula_routes.route('/formulas/<id>', methods=['GET'])
@jwt_required()
@doctor_required
def get_formula(id):
    formula = Formula.query.get(id)
    return jsonify(formula_schema.dump(formula))

@formula_routes.route('/formulas', methods=['POST'])
@jwt_required()
@doctor_required
def add_formula():
    new_formula = Formula(
        name=request.json['name'],
        description=request.json['description'],
        ingredients=request.json['ingredients'],
        instructions=request.json['instructions'],
    )
    db.session.add(new_formula)
    db.session.commit()
    return jsonify(formula_schema.dump(new_formula))

@formula_routes.route('/formulas/<id>', methods=['PUT'])
@jwt_required()
@doctor_required
def update_formula(id):
    formula = Formula.query.get(id)
    formula.name = request.json['name']
    formula.description = request.json['description']
    formula.ingredients = request.json['ingredients']
    formula.instructions = request.json['instructions']
    db.session.commit()
    return jsonify(formula_schema.dump(formula))

@formula_routes.route('/formulas/<id>', methods=['DELETE'])
@jwt_required()
@doctor_required
def delete_formula(id):
    formula = Formula.query.get(id)
    db.session.delete(formula)
    db.session.commit()
    return jsonify(formula_schema.dump(formula))