import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QListWidget, QTreeWidget, QTreeWidgetItem, QMessageBox
from comanda.connection.connection import conectar_bd, cerrar_conexion

class DatabaseViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor de Tablas de la Base de Datos")
        self.setGeometry(100, 100, 800, 600)

        # Conectar a la base de datos
        self.connection, self.cursor = conectar_bd()

        # Layout principal
        main_layout = QHBoxLayout()

        # Frame para la lista de tablas
        frame_tablas = QWidget()
        tablas_layout = QVBoxLayout(frame_tablas)
        tablas_label = QLabel("Tablas en la base de datos:")
        tablas_layout.addWidget(tablas_label)
        self.tablas_listbox = QListWidget()
        tablas_layout.addWidget(self.tablas_listbox)
        self.tablas_listbox.itemClicked.connect(self.mostrar_tabla)
        main_layout.addWidget(frame_tablas)

        # Obtener la lista de tablas y llenar el Listbox
        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        for table in self.cursor.fetchall():
            self.tablas_listbox.addItem(table[0])

        # Frame para la contenido de la tabla
        self.frame_contenido = QWidget()  # Hacemos frame_contenido un atributo de la instancia
        self.contenido_layout = QVBoxLayout(self.frame_contenido)

        # Añadir título para la sección de contenido
        self.contenido_title = QLabel("Datos de la tabla seleccionada:")
        self.contenido_layout.addWidget(self.contenido_title)

        self.contenido_tree = QTreeWidget()
        self.contenido_layout.addWidget(self.contenido_tree)
        main_layout.addWidget(self.frame_contenido)

        # Set main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def mostrar_tabla(self):
        try:
            # Obtener la tabla seleccionada
            selected_item = self.tablas_listbox.currentItem()
            if not selected_item:
                return
            table_name = selected_item.text()

            # Limpiar la tabla anterior
            self.contenido_tree.clear()
            self.contenido_tree.setColumnCount(0)

            # Ejecutar consulta para obtener el contenido de la tabla
            self.cursor.execute(f"SELECT * FROM {table_name}")

            # Obtener los nombres de las columnas
            column_names = [desc[0] for desc in self.cursor.description]
            self.contenido_tree.setHeaderLabels(column_names)

            # Insertar filas en la tabla
            rows = self.cursor.fetchall()
            for row in rows:
                QTreeWidgetItem(self.contenido_tree, [str(cell) for cell in row])

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def closeEvent(self, event):
        cerrar_conexion(self.connection, self.cursor)
        event.accept()

    def limpiar_tabla(self):
        # Limpiar la tabla de contenido y establecer el título predeterminado
        self.contenido_tree.clear()
        self.contenido_tree.setColumnCount(0)
        self.contenido_title.setText("Datos de la tabla seleccionada:")

def main():
    app = QApplication(sys.argv)
    viewer = DatabaseViewer()
    viewer.limpiar_tabla()  # Limpia la tabla al inicio
    viewer.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
