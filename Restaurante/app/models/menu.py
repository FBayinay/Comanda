from app import db 

class Menu(db.Model):
    __tablename__ = 'menus'
    id_menu = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    fecha_inicio = db.Column(db.String(10), nullable=False)
    fecha_fin = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return (f'<Menu id={self.id_menu}, tipo={self.tipo}, fecha_inicio={self.fecha_inicio}, '
                f'fecha_fin={self.fecha_fin}>')