from marshmallow import fields, Schema, post_load
from app.models import User

class UserSchema(Schema):
    id_usuario = fields.Integer(dump_only=True)
    nombre = fields.String(required=True, validate=fields.Length(min=1, max=50))
    apellido = fields.String(required=True, validate=fields.Length(min=1, max=50))
    dni = fields.String(required=True, validate=fields.Length(equal=8))
    email = fields.Email(required=True, validate=fields.Length(max=100))
    calle = fields.String(required=True, validate=fields.Length(min=1, max=80))
    numero = fields.Integer(required=True)
    rol_id = fields.Integer(allow_none=True)  # Allow None if rol_id is optional
    id_accion = fields.Integer(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
