from typing import List, Optional
from app.models import Receipt
from app.repositories import ReceiptRepository

repository = ReceiptRepository()

class ReceiptService:
    """
    ReceiptService class
    """
    def __init__(self):
        pass

    def create_receipt(self, id_comanda: int, total: float, 
                       estado_pago: str = 'Pendiente', detalles_comanda: Optional[str] = None) -> Receipt:
        """
        Create a new receipt entry
        :param id_comanda: int
        :param total: float
        :param estado_pago: str
        :param detalles_comanda: Optional[str]
        :return: Receipt
        """
        receipt = Receipt(id_comanda=id_comanda, total=total, estado_pago=estado_pago, detalles_comanda=detalles_comanda)
        return repository.save(receipt)

    def get_all_receipts(self) -> List[Receipt]:
        """
        Get all receipt entries
        :return: List[Receipt]
        """
        return repository.all()

    def get_receipt_by_id(self, id: int) -> Optional[Receipt]:
        """
        Get a receipt entry by its ID
        :param id: int
        :return: Optional[Receipt]
        """
        return repository.find(id)

    def update_receipt(self, id: int, id_comanda: Optional[int] = None, 
                       fecha: Optional[str] = None, total: Optional[float] = None,
                       estado_pago: Optional[str] = None, detalles_comanda: Optional[str] = None) -> Optional[Receipt]:
        """
        Update an existing receipt entry
        :param id: int
        :param id_comanda: Optional[int]
        :param fecha: Optional[str]
        :param total: Optional[float]
        :param estado_pago: Optional[str]
        :param detalles_comanda: Optional[str]
        :return: Optional[Receipt]
        """
        receipt = self.get_receipt_by_id(id)
        if receipt:
            if id_comanda is not None:
                receipt.id_comanda = id_comanda
            if fecha is not None:
                receipt.fecha = fecha
            if total is not None:
                receipt.total = total
            if estado_pago is not None:
                receipt.estado_pago = estado_pago
            if detalles_comanda is not None:
                receipt.detalles_comanda = detalles_comanda
            return repository.update(receipt, id)
        return None

    def delete_receipt(self, id: int) -> None:
        """
        Delete a receipt entry by its ID
        :param id: int
        """
        repository.delete(id)
