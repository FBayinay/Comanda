from marshmallow import fields, Schema, post_load
from app.models.command import Command

class CommandSchema(Schema):
    id_comanda = fields.Integer(dump_only=True)
    id_mesa = fields.Integer(required=True)
    id_usuario = fields.Integer(required=True)
    fecha_inicio = fields.DateTime(dump_only=True)
    fecha_fin = fields.DateTime(allow_none=True)
    estado = fields.String(required=True, validate=fields.Length(min=1, max=50))

    @post_load
    def make_command(self, data, **kwargs):
        return Command(**data)
