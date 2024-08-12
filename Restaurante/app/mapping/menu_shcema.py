from marshmallow import fields, Schema, post_load
from app.models import Menu

class MenuSchema(Schema):
    id_menu = fields.Integer(dump_only=True)
    tipo = fields.String(required=True, validate=fields.Length(min=1, max=50))
    fecha_inicio = fields.String(required=True, validate=fields.Length(equal=10))
    fecha_fin = fields.String(allow_none=True, validate=fields.Length(equal=10))

    @post_load
    def make_menu(self, data, **kwargs):
        return Menu(**data)
