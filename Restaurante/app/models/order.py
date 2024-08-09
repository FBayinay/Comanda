from app import db
class Order(db.Model):
    __tablename__ = 'pedidos_alamcen_general'
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id_proveedor'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    precio_total = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return (f'<Order id={self.id_pedido}, id_usuario={self.id_usuario}, id_producto={self.id_producto}, '
                f'id_proveedor={self.id_proveedor}, cantidad={self.cantidad}, '
                f'precio_unitario={self.precio_unitario}, precio_total={self.precio_total}, fecha={self.fecha}>')
