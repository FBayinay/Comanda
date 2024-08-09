from app import db
class WarehouseMovement(db.Model):
    __tablename__ = 'movimientos_almacen'
    id_movimiento = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return (f'<WarehouseMovement id={self.id_movimiento}, id_usuario={self.id_usuario}, '
                f'id_producto={self.id_producto}, cantidad={self.cantidad}, fecha={self.fecha}>')
