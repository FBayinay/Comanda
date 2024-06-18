from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from .data_entry_logic import DataEntryLogic
from comanda.login.password_utils import hash_password  # Asegúrate de ajustar la ruta según la estructura de tus archivos
from comanda.connection.database_manager import DatabaseManager

class DataEntryDialog(QDialog):
    def __init__(self, table_name):
        super().__init__()
        self.setWindowTitle("Ingresar Datos")
        self.table_name = table_name

        layout = QVBoxLayout()
        self.inputs = []

        manager = DatabaseManager()
        column_names = manager.get_column_names(self.table_name)

        for column_name in column_names[1:]:  # Excluir la primera columna (id)
            label = QLabel(column_name)
            layout.addWidget(label)
            line_edit = QLineEdit()
            layout.addWidget(line_edit)
            self.inputs.append((column_name, line_edit))

        self.submit_button = QPushButton("Guardar")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        manager.close_connection()

    def submit_data(self):
        manager = DatabaseManager()
        data = {col_name: input.text() for col_name, input in self.inputs}
        if all(data.values()):
            try:
                if self.table_name == 'login':
                    data['password_hash'] = hash_password(data['password_hash'])

                manager.insert_data(self.table_name, data)
                QMessageBox.information(self, "Éxito", "Datos guardados correctamente.")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar los datos: {str(e)}")
            finally:
                manager.close_connection()
        else:
            QMessageBox.warning(self, "Advertencia", "Todos los campos deben ser completados.")
