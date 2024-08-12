from marshmallow import fields, Schema, post_load
from app.models import Product

class ProductSchema(Schema):
    id_producto = fields.Integer(dump_only=True)
    nombre = fields.String(required=True, validate=fields.Length(min=1, max=50))

    @post_load
    def make_product(self, data, **kwargs):
        return Product(**data)
