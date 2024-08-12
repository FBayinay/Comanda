from marshmallow import fields, Schema, post_load
from app.models import Order

class OrderSchema(Schema):
    id_pedido = fields.Integer(dump_only=True)
    id_usuario = fields.Integer(required=True)
    id_producto = fields.Integer(required=True)
    id_proveedor = fields.Integer(required=True)
    cantidad = fields.Integer(required=True)
    precio_unitario = fields.Decimal(as_string=True, required=True)
    precio_total = fields.Decimal(as_string=True, required=True)
    fecha = fields.DateTime(dump_only=True)

    @post_load
    def make_order(self, data, **kwargs):
        return Order(**data)
