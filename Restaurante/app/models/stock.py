from app import db
class Stock(db.Model):
    __tablename__ = 'stock'
    id_stock = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Stock id={self.id_stock}, id_producto={self.id_producto}, cantidad={self.cantidad}>'