from marshmallow import fields, Schema, post_load
from app.models.action import Action  

class ActionSchema(Schema):
    id_accion = fields.Integer(dump_only=True)  
    nombre = fields.String(required=True, validate=fields.Length(min=1, max=50))  

    @post_load
    def make_action(self, data, **kwargs):
        return Action(**data)  
