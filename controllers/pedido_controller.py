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
        self.ui.pushButton.clicked.connect(self.ver_plano)      # Botón Ver
        self.ui.pushButton_2.clicked.connect(self.adjuntar_plano)  # Botón Adjuntar
        
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

            datos = {
                'cliente_nombre': self.ui.Cliente.text(),
                'estado': self.ui.comboBox.currentText(),
                'fecha_medicion': self.ui.dateEdit.date().toString("yyyy-MM-dd"),
                'fecha_llegada_materiales': self.ui.dateEdit_3.date().toString("yyyy-MM-dd"),
                'fecha_entrega': self.ui.dateEdit_2.date().toString("yyyy-MM-dd"),
                'presupuesto': presupuesto,
                'notas': self.ui.plainTextEdit.toPlainText(),
                'ruta_plano': ''  # Agregamos el campo con un valor vacío
            }
            
            print("Datos a enviar:", datos)
            
            if self.pedido_id:
                # Obtener el pedido actual para mantener la ruta_plano existente
                pedido_actual = ApiService.get_pedido(self.pedido_id)
                if pedido_actual and pedido_actual.get('ruta_plano'):
                    datos['ruta_plano'] = pedido_actual['ruta_plano']
                
                response = requests.put(
                    f"{ApiService.BASE_URL}/pedidos/{self.pedido_id}/",
                    json=datos
                )
                print("Status code:", response.status_code)
                print("Respuesta del servidor:", response.text)
                
                if response.status_code in [200, 201]:
                    print(f"✅ Pedido {self.pedido_id} actualizado exitosamente")
                    self.pedido_actualizado.emit()
                else:
                    print(f"❌ Error al actualizar pedido: {response.status_code}")
                    print("Detalles del error:", response.text)
            else:
                response = requests.post(
                    f"{ApiService.BASE_URL}/pedidos/",
                    json=datos
                )
                print("Status code:", response.status_code)
                print("Respuesta del servidor:", response.text)
                
                if response.status_code in [200, 201]:
                    resultado = response.json()
                    self.pedido_id = resultado['id']
                    print(f"✅ Nuevo pedido creado con ID: {self.pedido_id}")
                    self.pedido_actualizado.emit()
                else:
                    print(f"❌ Error al crear pedido: {response.status_code}")
                    print("Detalles del error:", response.text)
            
        except Exception as e:
            print(f"Error al guardar los cambios: {str(e)}")

    def adjuntar_plano(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Plano",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp);;Todos los archivos (*.*)"
        )
        
        if archivo:
            try:
                # Crear un diccionario con el archivo para enviar
                with open(archivo, 'rb') as f:
                    files = {'plano': f}
                    # Aquí deberías tener un endpoint en tu API para subir archivos
                    response = requests.post(
                        f"{ApiService.BASE_URL}/pedidos/{self.pedido_id}/plano/",
                        files=files
                    )
                
                if response.status_code in [200, 201]:
                    print("✅ Plano subido exitosamente")
                    self.pedido_actualizado.emit()
                else:
                    print(f"❌ Error al subir el plano: {response.status_code}")
            
            except Exception as e:
                print(f"Error al subir el plano: {e}")
    
    def ver_plano(self):
        try:
            pedido = ApiService.get_pedido(self.pedido_id)
            
            if pedido and pedido.get('ruta_plano'):
                # Hacer una petición GET a la URL del plano
                response = requests.get(f"{ApiService.BASE_URL}/planos/{pedido['ruta_plano']}")
                
                if response.status_code == 200:
                    # Crear QPixmap desde los bytes de la imagen
                    image_data = BytesIO(response.content)
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data.getvalue())
                    
                    # Mostrar la imagen
                    self.ventana_imagen = QLabel()
                    pixmap = pixmap.scaled(800, 600, aspectRatioMode=1)
                    self.ventana_imagen.setPixmap(pixmap)
                    self.ventana_imagen.show()
                else:
                    print("No se pudo obtener el plano del servidor")
            else:
                print("Este pedido no tiene un plano adjunto")
                
        except Exception as e:
            print(f"Error al mostrar el plano: {e}")

    def __del__(self):
        # Cerrar la conexión cuando se destruye el objeto
        if hasattr(self, 'conn') and self.conn:
            self.conn.close() 