from app import ma
from marshmallow import fields

class FormulaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'ingredients', 'instructions', 'doctor_id')

formula_schema = FormulaSchema()
formulas_schema = FormulaSchema(many=True)
