import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from connection import conectar_bd, cerrar_conexion
import psycopg2

class DeleteEntryDialog(QDialog):
    def __init__(self, table_name, primary_key, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eliminar Fila")
        self.table_name = table_name
        self.primary_key = primary_key
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        label = QLabel(f"Ingrese el {self.primary_key} de la fila a eliminar:")
        layout.addWidget(label)
        self.id_edit = QLineEdit()
        layout.addWidget(self.id_edit)

        submit_button = QPushButton("Eliminar")
        submit_button.clicked.connect(self.confirm_delete)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def confirm_delete(self):
        row_id = self.id_edit.text()
        if row_id:
            confirm = QMessageBox.question(
                self,
                "Confirmación",
                f"¿Está seguro de que desea eliminar la fila con {self.primary_key} {row_id}? Esta acción es irreversible.",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                self.delete_row(row_id)
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese un ID válido.")

    def delete_row(self, row_id):
        try:
            connection, cursor = conectar_bd()
            delete_query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = %s"
            cursor.execute(delete_query, (row_id,))
            connection.commit()
            cerrar_conexion(connection, cursor)
            print(f"Fila con {self.primary_key} {row_id} eliminada correctamente de la base de datos.")
            self.accept()
        except (Exception, psycopg2.Error) as error:
            print("Error al eliminar la fila de la base de datos:", error)
            QMessageBox.critical(self, "Error", "Error al eliminar la fila de la base de datos.")
