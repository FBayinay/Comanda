from app import db   
class Table(db.Model):
    __tablename__ = 'mesas'
    id_mesa = db.Column(db.Integer, primary_key=True)
    numero_mesa = db.Column(db.Integer, nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return (f'<Table id={self.id_mesa}, numero_mesa={self.numero_mesa}, '
                f'capacidad={self.capacidad}, estado={self.estado}>')