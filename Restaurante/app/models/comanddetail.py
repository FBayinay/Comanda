class CommandDetail(db.Model):
    __tablename__ = 'detalles_comanda'
    id_detalles = db.Column(db.Integer, primary_key=True)
    id_comanda = db.Column(db.Integer, db.ForeignKey('comanda.id_comanda'), nullable=False)
    id_item_menu = db.Column(db.Integer, db.ForeignKey('items_menu.id_items'), nullable=False)
    id_menu = db.Column(db.Integer, db.ForeignKey('menus.id_menu'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_total = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return (f'<CommandDetail id={self.id_detalles}, id_comanda={self.id_comanda}, '
                f'id_item_menu={self.id_item_menu}, id_menu={self.id_menu}, '
                f'cantidad={self.cantidad}, precio_total={self.precio_total}>')
