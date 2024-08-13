from app import db 

class MenuCategory(db.Model):
    __tablename__ = 'categorias_menu'
    id_categoria = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return (f'<MenuCategory id={self.id_categoria}, categoria={self.categoria}, '
                f'descripcion={self.descripcion}>')
