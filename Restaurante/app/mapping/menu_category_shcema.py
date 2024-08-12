from marshmallow import fields, Schema, post_load
from app.models import MenuCategory

class MenuCategorySchema(Schema):
    id_categoria = fields.Integer(dump_only=True)
    categoria = fields.String(required=True, validate=fields.Length(min=1, max=50))
    descripcion = fields.String(required=True, validate=fields.Length(min=1, max=50))

    @post_load
    def make_menu_category(self, data, **kwargs):
        return MenuCategory(**data)
