from marshmallow import fields, Schema, post_load
from app.models import WarehouseMovement

class WarehouseMovementSchema(Schema):
    id_movimiento = fields.Integer(dump_only=True)
    id_usuario = fields.Integer(required=True)
    id_producto = fields.Integer(required=True)
    cantidad = fields.Integer(required=True)
    fecha = fields.DateTime(dump_only=True)

    @post_load
    def make_warehouse_movement(self, data, **kwargs):
        return WarehouseMovement(**data)
