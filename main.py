import sys
from PyQt5.QtWidgets import QApplication
from controllers.login_controller import LoginController
from services.api_service import ApiService

def main():
    app = QApplication(sys.argv)  # Crear la instancia de QApplication
    api_service = ApiService()  # Crear una instancia de ApiService
    login_controller = LoginController(api_service)  # Crear una instancia de LoginController
    login_controller.mostrar_login()  # Mostrar el formulario de login y procesar
    sys.exit(app.exec_())  # Iniciar el loop de eventos aquí

if __name__ == "__main__":
    main()
    