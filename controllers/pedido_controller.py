from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel
from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtGui import QPixmap
from ui.ventana_pedido import Ui_MainWindow
from services.api_service import ApiService
import os
import requests
from io import BytesIO

class PedidoController(QMainWindow):
    # Agregar señal de actualización
    pedido_actualizado = pyqtSignal()
    
    def __init__(self, pedido_id=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pedido_id = pedido_id
        
        # Conectar botones
        self.ui.pushButton_3.clicked.connect(self.guardar_cambios)
        
        
        if self.pedido_id:
            self.cargar_pedido()
    
    def cargar_pedido(self):
        pedido = ApiService.get_pedido(self.pedido_id)
        
        if pedido:
            # Establecer los valores en los widgets
            self.ui.Cliente.setText(pedido['cliente_nombre'])
            self.ui.comboBox.setCurrentText(pedido['estado'])
            
            # Convertir strings de fecha a QDate y establecerlos
            self.ui.dateEdit.setDate(QDate.fromString(pedido['fecha_medicion'], "yyyy-MM-dd"))
            self.ui.dateEdit_3.setDate(QDate.fromString(pedido['fecha_llegada_materiales'], "yyyy-MM-dd"))
            self.ui.dateEdit_2.setDate(QDate.fromString(pedido['fecha_entrega'], "yyyy-MM-dd"))
            
            self.ui.lineEdit_11.setText(str(pedido['presupuesto']))
            
            if pedido['notas']:
                self.ui.plainTextEdit.setPlainText(pedido['notas'])
    
    def guardar_cambios(self):
        try:
            # Validar el presupuesto antes de convertirlo
            presupuesto_texto = self.ui.lineEdit_11.text()
            try:
                presupuesto = float(presupuesto_texto) if presupuesto_texto else 0.0
            except ValueError:
                print("Error: El presupuesto debe ser un número válido")
                return

            # Crear un diccionario con los datos del pedido actualizado
            datos = {
                'cliente_nombre': self.ui.Cliente.text(),
                'estado': self.ui.comboBox.currentText(),
                'fecha_medicion': self.ui.dateEdit.date().toString("yyyy-MM-dd"),
                'fecha_llegada_materiales': self.ui.dateEdit_3.date().toString("yyyy-MM-dd"),
                'fecha_entrega': self.ui.dateEdit_2.date().toString("yyyy-MM-dd"),
                'presupuesto': presupuesto,
                'notas': self.ui.plainTextEdit.toPlainText(),
                'ruta_plano': ''  # Este campo será vacío si no se ha adjuntado un plano
            }

            print("Datos a enviar:", datos)

            if self.pedido_id:
                # Llamamos a la función para actualizar el pedido en la API
                pedido_actualizado = ApiService.actualizar_pedido(self.pedido_id, datos)

                if pedido_actualizado:
                    print(f"✅ Pedido {self.pedido_id} actualizado exitosamente")
                    self.pedido_actualizado.emit()  # Emitimos la señal para actualizar la vista
                else:
                    print(f"❌ Error al actualizar pedido")
            else:
                print("No se puede actualizar. Pedido ID no disponible.")
        
        except Exception as e:
            print(f"Error al guardar los cambios: {str(e)}")


    def __del__(self):
        # Cerrar la conexión cuando se destruye el objeto
        if hasattr(self, 'conn') and self.conn:
            self.conn.close() 