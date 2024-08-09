from app import db
class Action(db.Model):
    __tablename__ = 'acciones'
    id_accion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Action id={self.id_accion}, nombre={self.nombre}>'
