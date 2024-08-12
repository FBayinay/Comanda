from typing import List, Optional
from app.models import CommandDetail  # Importar desde app/models
from app import db

class CommandDetailRepository:
    # Guardar un nuevo detalle de comando en la base de datos
    def save(self, command_detail: CommandDetail) -> CommandDetail:
        db.session.add(command_detail)  # Añadir el objeto CommandDetail a la sesión de base de datos
        db.session.commit()    # Confirmar (commit) la transacción para guardar los cambios
        return command_detail  # Retornar el objeto CommandDetail guardado

    # Actualizar un detalle de comando existente en la base de datos
    def update(self, command_detail: CommandDetail, id: int) -> Optional[CommandDetail]:
        entity = self.find(id)  # Buscar el detalle de comando existente por ID
        if entity is None:
            return None         # Si no se encuentra el detalle, retornar None
        entity.id_comanda = command_detail.id_comanda
        entity.id_item_menu = command_detail.id_item_menu
        entity.id_menu = command_detail.id_menu
        entity.cantidad = command_detail.cantidad
        entity.precio_total = command_detail.precio_total
        db.session.commit()   # Confirmar los cambios
        return entity         # Retornar el detalle de comando actualizado

    # Eliminar un detalle de comando de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  # Buscar el detalle de comando existente por ID
        if entity:
            db.session.delete(entity)  # Eliminar el detalle de comando de la sesión de base de datos
            db.session.commit()        # Confirmar la transacción

    # Obtener todos los detalles de comando de la base de datos
    def all(self) -> List[CommandDetail]:
        return db.session.query(CommandDetail).all()  # Obtener y retornar todos los detalles

    # Buscar un detalle de comando por ID
    def find(self, id: int) -> Optional[CommandDetail]:
        return db.session.query(CommandDetail).filter(CommandDetail.id_detalles == id).one_or_none()  
        # Buscar el detalle de comando por ID y retornar uno o ninguno (si no se encuentra)
