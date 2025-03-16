import sys
from PyQt5.QtWidgets import QApplication
from controllers.login_controller import LoginController
from services.api_service import ApiService

def main():
    api_service = ApiService()  # Crear una instancia de ApiService
    login_controller = LoginController(api_service)  # Crear una instancia de LoginController
    login_controller.mostrar_login()  # Mostrar el formulario de login y procesar

if __name__ == "__main__":
    main()


#if __name__ == "__main__":
#   app = QApplication(sys.argv)
# ventana = HomeController()
# ventana.show()
    #sys.exit(app.exec_())

