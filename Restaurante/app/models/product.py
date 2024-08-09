from app import db
class Product(db.Model):
    __tablename__ = 'productos'
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Product id={self.id_producto}, nombre={self.nombre}>'
    