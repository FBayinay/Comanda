from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from .data_entry_logic import DataEntryLogic
from comanda.login.password_utils import hash_password  # Asegúrate de ajustar la ruta según la estructura de tus archivos
from comanda.connection.database_manager import DatabaseManager

class DataEntryDialog(QDialog):
    def __init__(self, table_name):
        super().__init__()
        self.setWindowTitle("Ingresar Datos")
        self.table_name = table_name
        self.column_names = DatabaseManager().get_column_names(self.table_name)  # Asigna column_names a self.column_names

        layout = QVBoxLayout()
        self.inputs = []

        for column_name in self.column_names[1:]:  # Excluye la primera columna (id)
            label = QLabel(column_name)
            layout.addWidget(label)
            line_edit = QLineEdit()
            layout.addWidget(line_edit)
            self.inputs.append(line_edit)

        self.submit_button = QPushButton("Guardar")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_data(self):
        data = {column_name: input.text() for column_name, input in zip(self.column_names[1:], self.inputs)}
        if all(data.values()):
            try:
                if self.table_name == 'login':  # Si estamos ingresando datos en la tabla 'login'
                    # Aplicar hash a la contraseña
                    data['password_hash'] = hash_password(data['password_hash'])  # Ajusta según tu estructura de datos

                DatabaseManager().insert_data(self.table_name, data)  # Inserta los datos usando DatabaseManager
                QMessageBox.information(self, "Éxito", "Datos guardados correctamente.")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar los datos: {str(e)}")
        else:
            QMessageBox.warning(self, "Advertencia", "Todos los campos deben ser completados.")
