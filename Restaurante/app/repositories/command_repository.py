from typing import List, Optional
from app.models import Command  # Importar desde app/models
from app import db

class CommandRepository:
    # Guardar un nuevo comando en la base de datos
    def save(self, command: Command) -> Command:
        db.session.add(command)  # Añadir el objeto Command a la sesión de base de datos
        db.session.commit()    # Confirmar (commit) la transacción para guardar los cambios
        return command         # Retornar el objeto Command guardado

    # Actualizar un comando existente en la base de datos
    def update(self, command: Command, id: int) -> Optional[Command]:
        entity = self.find(id)  # Buscar el comando existente por ID
        if entity is None:
            return None         # Si no se encuentra el comando, retornar None
        entity.id_mesa = command.id_mesa
        entity.id_usuario = command.id_usuario
        entity.fecha_inicio = command.fecha_inicio
        entity.fecha_fin = command.fecha_fin
        entity.estado = command.estado
        db.session.commit()   # Confirmar los cambios
        return entity         # Retornar el comando actualizado

    # Eliminar un comando de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  # Buscar el comando existente por ID
        if entity:
            db.session.delete(entity)  # Eliminar el comando de la sesión de base de datos
            db.session.commit()        # Confirmar la transacción

    # Obtener todos los comandos de la base de datos
    def all(self) -> List[Command]:
        return db.session.query(Command).all()  # Obtener y retornar todos los comandos

    # Buscar un comando por ID
    def find(self, id: int) -> Optional[Command]:
        return db.session.query(Command).filter(Command.id_comanda == id).one_or_none()  
        # Buscar el comando por ID y retornar uno o ninguno (si no se encuentra)
