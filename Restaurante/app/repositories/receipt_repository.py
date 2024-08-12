from typing import List, Optional
from app.models import Receipt  # Importar desde app/models
from app import db

class ReceiptRepository:
    # Guardar un nuevo recibo en la base de datos
    def save(self, receipt: Receipt) -> Receipt:
        db.session.add(receipt)  # Añadir el objeto Receipt a la sesión de base de datos
        db.session.commit()    # Confirmar (commit) la transacción para guardar los cambios
        return receipt  # Retornar el objeto Receipt guardado

    # Actualizar un recibo existente en la base de datos
    def update(self, receipt: Receipt, id: int) -> Optional[Receipt]:
        entity = self.find(id)  # Buscar el recibo existente por ID
        if entity is None:
            return None         # Si no se encuentra el recibo, retornar None
        entity.id_comanda = receipt.id_comanda
        entity.fecha = receipt.fecha
        entity.total = receipt.total
        entity.estado_pago = receipt.estado_pago
        entity.detalles_comanda = receipt.detalles_comanda
        db.session.commit()   # Confirmar los cambios
        return entity         # Retornar el recibo actualizado

    # Eliminar un recibo de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  # Buscar el recibo existente por ID
        if entity:
            db.session.delete(entity)  # Eliminar el recibo de la sesión de base de datos
            db.session.commit()        # Confirmar la transacción

    # Obtener todos los recibos de la base de datos
    def all(self) -> List[Receipt]:
        return db.session.query(Receipt).all()  # Obtener y retornar todos los recibos

    # Buscar un recibo por ID
    def find(self, id: int) -> Optional[Receipt]:
        return db.session.query(Receipt).filter(Receipt.id_recibo == id).one_or_none()  
        # Buscar el recibo por ID y retornar uno o ninguno (si no se encuentra)
