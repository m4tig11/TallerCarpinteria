import sys
from PyQt5.QtWidgets import QApplication
from controllers.home_controller import HomeController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = HomeController()
    ventana.show()
    sys.exit(app.exec_())

