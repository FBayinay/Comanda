from typing import List, Optional
from app.models import Supplier
from app.repositories import SupplierRepository

repository = SupplierRepository()

class SupplierService:
    """
    SupplierService class
    """
    def __init__(self):
        pass

    def create_supplier(self, nombre: str, contacto: str) -> Supplier:
        """
        Create a new supplier entry
        :param nombre: str
        :param contacto: str
        :return: Supplier
        """
        supplier = Supplier(nombre=nombre, contacto=contacto)
        return repository.save(supplier)

    def get_all_suppliers(self) -> List[Supplier]:
        """
        Get all supplier entries
        :return: List[Supplier]
        """
        return repository.all()

    def get_supplier_by_id(self, id: int) -> Optional[Supplier]:
        """
        Get a supplier entry by its ID
        :param id: int
        :return: Optional[Supplier]
        """
        return repository.find(id)

    def update_supplier(self, id: int, nombre: Optional[str] = None, contacto: Optional[str] = None) -> Optional[Supplier]:
        """
        Update an existing supplier entry
        :param id: int
        :param nombre: Optional[str]
        :param contacto: Optional[str]
        :return: Optional[Supplier]
        """
        supplier = self.get_supplier_by_id(id)
        if supplier:
            if nombre is not None:
                supplier.nombre = nombre
            if contacto is not None:
                supplier.contacto = contacto
            return repository.update(supplier, id)
        return None

    def delete_supplier(self, id: int) -> None:
        """
        Delete a supplier entry by its ID
        :param id: int
        """
        repository.delete(id)
