from marshmallow import fields, Schema, post_load
from app.models import Receipt

class ReceiptSchema(Schema):
    id_recibo = fields.Integer(dump_only=True)
    id_comanda = fields.Integer(required=True)
    fecha = fields.DateTime(dump_only=True)
    total = fields.Decimal(as_string=True, required=True)
    estado_pago = fields.String(required=True, validate=fields.Length(min=1, max=50))
    detalles_comanda = fields.String(allow_none=True)

    @post_load
    def make_receipt(self, data, **kwargs):
        return Receipt(**data)
