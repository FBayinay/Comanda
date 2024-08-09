from app import db
class User(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(8), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    calle = db.Column(db.String(80), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id_rol'))
    id_accion = db.Column(db.Integer, db.ForeignKey('acciones.id_accion'), nullable=False)

    def __repr__(self):
        return (f'<User id={self.id_usuario}, nombre={self.nombre}, apellido={self.apellido}, '
                f'dni={self.dni}, email={self.email}, calle={self.calle}, numero={self.numero}, '
                f'rol_id={self.rol_id}, id_accion={self.id_accion}>')
