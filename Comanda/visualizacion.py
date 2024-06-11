import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QListWidget, QTreeWidget, QTreeWidgetItem, QPushButton, QMessageBox, QDialog
from PySide6 import QtCore  # Importa QtCore para usar AlignTop
from data_entry_ui import DataEntryDialog
from database_manager import DatabaseManager

class TableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.itemClicked.connect(parent.mostrar_tabla)

class DatabaseViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor de Tablas de la Base de Datos")
        self.setGeometry(100, 100, 800, 600)

        self.manager = DatabaseManager()

        main_layout = QHBoxLayout()

        frame_tablas = QWidget()
        tablas_layout = QVBoxLayout(frame_tablas)
        tablas_label = QLabel("Tablas en la base de datos:")
        tablas_layout.addWidget(tablas_label)
        self.tablas_listbox = TableListWidget(self)
        tablas_layout.addWidget(self.tablas_listbox)
        main_layout.addWidget(frame_tablas)

        self.frame_contenido = QWidget()
        contenido_layout = QVBoxLayout(self.frame_contenido)
        contenido_layout.setAlignment(QtCore.Qt.AlignTop)  # Alineación arriba
        self.contenido_title = QLabel("Datos de la tabla seleccionada:")
        contenido_layout.addWidget(self.contenido_title)
        self.contenido_tree = QTreeWidget()
        contenido_layout.addWidget(self.contenido_tree)

        # Layout para los botones dentro del área de datos
        buttons_layout = QHBoxLayout()

        # Agrega un espacio elástico para empujar los botones a la derecha
        buttons_layout.addStretch()

        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(30, 30)  # Establece el tamaño del botón "+"
        self.add_button.clicked.connect(self.add_row)
        buttons_layout.addWidget(self.add_button)

        self.subtract_button = QPushButton("-")
        self.subtract_button.setFixedSize(30, 30)  # Establece el tamaño del botón "-"
        self.subtract_button.clicked.connect(self.subtract_row)
        buttons_layout.addWidget(self.subtract_button)

        contenido_layout.addLayout(buttons_layout)  # Agregar botones al layout del área de datos

        main_layout.addWidget(self.frame_contenido)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.limpiar_tabla()  # Limpiar la tabla al inicio
        self.populate_table_list()

    def populate_table_list(self):
        table_names = self.manager.get_table_names()
        for table_name in table_names:
            self.tablas_listbox.addItem(table_name)

    def mostrar_tabla(self, item):
        try:
            table_name = item.text()
            self.selected_table_name = table_name  # Guarda el nombre de la tabla seleccionada
            column_names, rows = self.manager.get_table_data(table_name)
            self.display_table_data(column_names, rows)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_table_data(self, column_names, rows):
        self.contenido_tree.clear()
        self.contenido_tree.setColumnCount(len(column_names))
        self.contenido_tree.setHeaderLabels(column_names)
        for row in rows:
            QTreeWidgetItem(self.contenido_tree, [str(cell) for cell in row])

    def limpiar_tabla(self):
        self.contenido_tree.clear()
        self.contenido_tree.setColumnCount(0)
        self.contenido_title.setText("Datos de la tabla seleccionada:")
        
    def add_row(self):
        try:
            # Obtén los nombres de las columnas de la tabla seleccionada
            column_names = self.manager.get_column_names(self.selected_table_name)
            # Abre la ventana de ingreso de datos pasando el nombre de la tabla seleccionada y las columnas
            dialog = DataEntryDialog(self.selected_table_name, column_names, self)
            if dialog.exec() == QDialog.Accepted:
                print("Datos guardados correctamente.")
                # Refrescar la tabla después de guardar los datos
                self.mostrar_tabla(self.tablas_listbox.currentItem())
            else:
                print("Ingreso de datos cancelado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def subtract_row(self):
        # Lógica para eliminar una fila
        pass

    def closeEvent(self, event):
        self.manager.close_connection()
        event.accept()

def main():
    app = QApplication(sys.argv)
    viewer = DatabaseViewer()
    viewer.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
