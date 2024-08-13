from app import db 
class MenuItem(db.Model):
    __tablename__ = 'items_menu'
    id_items = db.Column(db.Integer, primary_key=True)
    id_menu = db.Column(db.Integer, db.ForeignKey('menus.id_menu'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias_menu.id_categoria'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return (f'<MenuItem id={self.id_items}, id_menu={self.id_menu}, id_categoria={self.id_categoria}, '
                f'nombre={self.nombre}, descripcion={self.descripcion}, precio={self.precio}>')
