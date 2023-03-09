from flask import Blueprint, jsonify, request
from database import db
from models.formula import Formula
from schemas.formula_schema import formula_schema, formulas_schema

formula_routes = Blueprint('formula_routes', __name__, url_prefix='/')

@formula_routes.route('/formulas', methods=['GET'])
def get_formulas():
    formulas = Formula.query.all()
    return jsonify(formulas_schema.dump(formulas))

@formula_routes.route('/formulas/<id>', methods=['GET'])
def get_formula(id):
    formula = Formula.query.get(id)
    return jsonify(formula_schema.dump(formula))

@formula_routes.route('/formulas', methods=['POST'])
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