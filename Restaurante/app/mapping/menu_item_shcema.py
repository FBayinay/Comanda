from marshmallow import fields, Schema, post_load
from app.models import MenuItem

class MenuItemSchema(Schema):
    id_items = fields.Integer(dump_only=True)
    id_menu = fields.Integer(required=True)
    id_categoria = fields.Integer(required=True)
    nombre = fields.String(required=True, validate=fields.Length(min=1, max=100))
    descripcion = fields.String(allow_none=True, validate=fields.Length(max=200))
    precio = fields.Decimal(as_string=True, required=True)

    @post_load
    def make_menu_item(self, data, **kwargs):
        return MenuItem(**data)
