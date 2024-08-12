from typing import List, Optional
from app.models.table import Table
from app import db

class TableRepository:
    # Guardar una nueva mesa en la base de datos
    def save(self, table: Table) -> Table:
        db.session.add(table)
        db.session.commit()
        return table

    # Actualizar una mesa existente en la base de datos
    def update(self, table: Table, id: int) -> Optional[Table]:
        entity = self.find(id)
        if entity is None:
            return None
        entity.numero_mesa = table.numero_mesa
        entity.capacidad = table.capacidad
        entity.estado = table.estado
        db.session.commit()
        return entity

    # Eliminar una mesa de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)
        if entity:
            db.session.delete(entity)
            db.session.commit()

    # Obtener todas las mesas de la base de datos
    def all(self) -> List[Table]:
        return db.session.query(Table).all()

    # Buscar una mesa por ID
    def find(self, id: int) -> Optional[Table]:
        return db.session.query(Table).filter(Table.id_mesa == id).one_or_none()
