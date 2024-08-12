from marshmallow import fields, Schema, post_load
from app.models import Table

class TableSchema(Schema):
    id_mesa = fields.Integer(dump_only=True)
    numero_mesa = fields.Integer(required=True)
    capacidad = fields.Integer(required=True)
    estado = fields.String(required=True, validate=fields.Length(min=1, max=20))

    @post_load
    def make_table(self, data, **kwargs):
        return Table(**data)
