from app import db
class Login(db.Model):
    __tablename__ = 'login'
    id_login = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Login id={self.id_login}, id_usuario={self.id_usuario}, username={self.username}>'
