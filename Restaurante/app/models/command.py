from app import db 
class Command(db.Model):
    __tablename__ = 'comanda'
    id_comanda = db.Column(db.Integer, primary_key=True)
    id_mesa = db.Column(db.Integer, db.ForeignKey('mesas.id_mesa'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    fecha_fin = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.String(50), nullable=False, default='En Proceso')

    def __repr__(self):
        return (f'<Command id={self.id_comanda}, id_mesa={self.id_mesa}, id_usuario={self.id_usuario}, '
                f'fecha_inicio={self.fecha_inicio}, fecha_fin={self.fecha_fin}, estado={self.estado}>')
