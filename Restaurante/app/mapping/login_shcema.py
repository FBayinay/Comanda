from marshmallow import fields, Schema, post_load
from app.models import Login

class LoginSchema(Schema):
    id_login = fields.Integer(dump_only=True)
    id_usuario = fields.Integer(required=True)
    username = fields.String(required=True, validate=fields.Length(min=1, max=50))
    password_hash = fields.String(required=True, validate=fields.Length(min=1, max=100))

    @post_load
    def make_login(self, data, **kwargs):
        return Login(**data)
