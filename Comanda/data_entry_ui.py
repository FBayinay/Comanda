import sys
import psycopg2
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from data_entry_logic import DataEntryLogic
from connection import conectar_bd, cerrar_conexion

class DataEntryDialog(QDialog):
    def __init__(self, table_name, column_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ingreso de Datos")
        self.table_name = table_name
        self.column_names = column_names
        self.logic = DataEntryLogic(column_names)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        for column_name in self.column_names[1:]:  # Excluir la primera columna (autoincremental)
            label = QLabel(f"Ingrese {column_name}:")
            line_edit = QLineEdit()
            layout.addWidget(label)
            layout.addWidget(line_edit)
            setattr(self, f"{column_name}_edit", line_edit)  # Añadir el QLineEdit como atributo de la instancia

        submit_button = QPushButton("Guardar")
        submit_button.clicked.connect(self.save_data)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def save_data(self):
        for column_name in self.column_names[1:]:
            line_edit = getattr(self, f"{column_name}_edit")
            data = line_edit.text()
            self.logic.enter_data(self.column_names.index(column_name), data)

        if self.logic.validate_data():
            entered_data = self.logic.get_entered_data()
            try:
                connection, cursor = conectar_bd()
                column_names_str = ', '.join(entered_data.keys())
                placeholders = ', '.join(['%s' for _ in entered_data.values()])
                insert_query = f"INSERT INTO {self.table_name} ({column_names_str}) VALUES ({placeholders})"
                cursor.execute(insert_query, list(entered_data.values()))
                connection.commit()
                cerrar_conexion(connection, cursor)
                print("Datos ingresados correctamente en la base de datos.")
                self.accept()
            except (Exception, psycopg2.Error) as error:
                print("Error al guardar datos en la base de datos:", error)
                QMessageBox.critical(self, "Error", "Error al guardar datos en la base de datos.")
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")
