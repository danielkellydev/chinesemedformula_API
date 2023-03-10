from app import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'password', 'admin')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

