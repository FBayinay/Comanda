from app import db 
class Receipt(db.Model):
    __tablename__ = 'recibo_cliente'
    id_recibo = db.Column(db.Integer, primary_key=True)
    id_comanda = db.Column(db.Integer, db.ForeignKey('comanda.id_comanda'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado_pago = db.Column(db.String(50), nullable=False, default='Pendiente')
    detalles_comanda = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return (f'<Receipt id={self.id_recibo}, id_comanda={self.id_comanda}, fecha={self.fecha}, '
                f'total={self.total}, estado_pago={self.estado_pago}, detalles_comanda={self.detalles_comanda}>')
