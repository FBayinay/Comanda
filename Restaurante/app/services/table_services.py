from typing import List, Optional
from app.models import Table
from app.repositories import TableRepository

repository = TableRepository()

class TableService:
    """
    TableService class
    """
    def __init__(self):
        pass

    def create_table(self, numero_mesa: int, capacidad: int, estado: str) -> Table:
        """
        Create a new table entry
        :param numero_mesa: int
        :param capacidad: int
        :param estado: str
        :return: Table
        """
        table = Table(numero_mesa=numero_mesa, capacidad=capacidad, estado=estado)
        return repository.save(table)

    def get_all_tables(self) -> List[Table]:
        """
        Get all table entries
        :return: List[Table]
        """
        return repository.all()

    def get_table_by_id(self, id: int) -> Optional[Table]:
        """
        Get a table entry by its ID
        :param id: int
        :return: Optional[Table]
        """
        return repository.find(id)

    def update_table(self, id: int, numero_mesa: Optional[int] = None, 
                     capacidad: Optional[int] = None, estado: Optional[str] = None) -> Optional[Table]:
        """
        Update an existing table entry
        :param id: int
        :param numero_mesa: Optional[int]
        :param capacidad: Optional[int]
        :param estado: Optional[str]
        :return: Optional[Table]
        """
        table = self.get_table_by_id(id)
        if table:
            if numero_mesa is not None:
                table.numero_mesa = numero_mesa
            if capacidad is not None:
                table.capacidad = capacidad
            if estado is not None:
                table.estado = estado
            return repository.update(table, id)
        return None

    def delete_table(self, id: int) -> None:
        """
        Delete a table entry by its ID
        :param id: int
        """
        repository.delete(id)
