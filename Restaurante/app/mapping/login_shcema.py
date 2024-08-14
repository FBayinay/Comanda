from marshmallow import fields, Schema, post_load, pre_dump
from app.models import Login

class LoginSchema(Schema):
    id_login = fields.Integer(dump_only=True)
    id_usuario = fields.Integer(required=True)
    username = fields.String(required=True, validate=fields.Length(min=1, max=50))
    password = fields.String(load_only=True, validate=fields.Length(min=8, max=100))  # Validación solo al cargar

    @post_load
    def make_login(self, data, **kwargs):
        return Login(**data)

    @pre_dump
    def remove_password_hash(self, data, **kwargs):
        data.password_hash = None
        return data
