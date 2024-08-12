from marshmallow import fields, Schema, post_load
from app.models import Stock

class StockSchema(Schema):
    id_stock = fields.Integer(dump_only=True)
    id_producto = fields.Integer(required=True)
    cantidad = fields.Integer(required=True)

    @post_load
    def make_stock(self, data, **kwargs):
        return Stock(**data)
