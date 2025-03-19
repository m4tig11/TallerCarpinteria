import sys
from controllers import home_controller
import services.api_service
from PyQt5.QtWidgets import QApplication


class LoginController:
    def __init__(self, api_service):
        self.api_service = api_service
        self.ventana_home = None

    def mostrar_login(self):
        # Aquí mostrarías el formulario para que el usuario ingrese sus datos
        username = input("Ingrese su nombre de usuario: ")
        password = input("Ingrese su contraseña: ")

        # Llamar al método de login con las credenciales
        token = self.iniciar_sesion(username, password)

        if token:
            print("Inicio de sesión exitoso!")
            # Redirigir a la pantalla principal o continuar el flujo
            self.redirigir_a_home()
        else:
            print("Error en el inicio de sesión.")
            # Mostrar mensaje de error y permitir reintentar

    def iniciar_sesion(self, username, password):
        return self.api_service.login(username, password)

    def redirigir_a_home(self):
        # Lógica para redirigir a la pantalla principal (Home)
        print("Bienvenido a la página principal!")
        self.ventana_home = home_controller.HomeController()
        self.ventana_home.show()

