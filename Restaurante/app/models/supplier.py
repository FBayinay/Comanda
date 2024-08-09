from app import db
class Supplier(db.Model):
    __tablename__ = 'proveedores'
    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Supplier id={self.id_proveedor}, nombre={self.nombre}, contacto={self.contacto}>'
