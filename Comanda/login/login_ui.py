# login_ui.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QMessageBox
from comanda.login.login_manager import LoginManager
from comanda.login.role_authenticator import RoleAuthenticator

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.setGeometry(100, 100, 400, 200)

        self.manager = LoginManager()

        main_layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        main_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(self.password_input)

        login_button = QPushButton("Iniciar Sesión")
        login_button.clicked.connect(self.login)
        main_layout.addWidget(login_button)

        self.status_label = QLabel()
        main_layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor ingrese usuario y contraseña.")
            return

        user_data = self.manager.authenticate_user(username, password)

        if user_data:
            user_id, nombre, apellido, rol_id = user_data
            if RoleAuthenticator.check_role(user_data, 1):  # Verifica si el usuario es un Propietario
                self.status_label.setText(f"Inicio de sesión exitoso como {nombre} {apellido}")
                # Aquí puedes continuar con la lógica de tu aplicación después del inicio de sesión exitoso
                self.open_database_viewer()
            else:
                self.status_label.setText("Acceso denegado. No tienes los permisos necesarios.")
        else:
            self.status_label.setText("Inicio de sesión fallido. Verifique sus credenciales.")

    def open_database_viewer(self):
        from comanda.visualization.visualization import DatabaseViewer
        self.database_viewer = DatabaseViewer()
        self.database_viewer.show()
        self.close()

    def closeEvent(self, event):
        self.manager.close_connection()
        event.accept()

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
