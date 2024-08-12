from marshmallow import fields, Schema, post_load
from app.models import Supplier

class SupplierSchema(Schema):
    id_proveedor = fields.Integer(dump_only=True)
    nombre = fields.String(required=True, validate=fields.Length(min=1, max=50))
    contacto = fields.String(required=True, validate=fields.Length(min=1, max=20))

    @post_load
    def make_supplier(self, data, **kwargs):
        return Supplier(**data)
