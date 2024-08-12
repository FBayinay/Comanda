from marshmallow import fields, Schema, post_load
from app.models import CommandDetail

class CommandDetailSchema(Schema):
    id_detalles = fields.Integer(dump_only=True)
    id_comanda = fields.Integer(required=True)
    id_item_menu = fields.Integer(required=True)
    id_menu = fields.Integer(required=True)
    cantidad = fields.Integer(required=True)
    precio_total = fields.Decimal(as_string=True, required=True)

    @post_load
    def make_command_detail(self, data, **kwargs):
        return CommandDetail(**data)