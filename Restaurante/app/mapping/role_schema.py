from marshmallow import fields, Schema, post_load
from app.models.roles import Role

class RoleSchema(Schema):
    id_rol = fields.Integer(dump_only=True)
    nombre = fields.String(required=True, validate=fields.Length(min=1, max=50))

    @post_load
    def make_role(self, data, **kwargs):
        return Role(**data)
