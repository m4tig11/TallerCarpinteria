from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel, QMessageBox
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
        self.plano_temp = None  # Para almacenar temporalmente la imagen seleccionada
        
        # Conectar botones
        self.ui.pushButton_3.clicked.connect(self.guardar_cambios)
        self.ui.pushButton.clicked.connect(self.ver_plano)
        self.ui.pushButton_2.clicked.connect(self.adjuntar_plano)
        
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
    
    def adjuntar_plano(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Plano",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp);;Todos los archivos (*.*)"
        )
        
        if archivo:
            try:
                # Guardar la ruta del archivo temporalmente
                self.plano_temp = archivo
                QMessageBox.information(self, "Éxito", "Plano seleccionado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al seleccionar el plano: {str(e)}")
    
    def ver_plano(self):
        try:
            pedido = ApiService.get_pedido(self.pedido_id)
            
            if pedido and pedido.get('plano'):
                # Obtener la URL completa de la imagen
                imagen_url = pedido['plano']  # La URL ya viene completa del servidor
                
                print(f"Intentando cargar imagen desde: {imagen_url}")  # Debug
                
                # Hacer la petición para obtener la imagen
                headers = ApiService.get_auth_headers()  # Incluir el token de autenticación
                response = requests.get(imagen_url, headers=headers)
                
                print(f"Código de respuesta: {response.status_code}")  # Debug
                
                if response.status_code == 200:
                    # Crear QPixmap desde los bytes de la imagen
                    image_data = BytesIO(response.content)
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data.getvalue())
                    
                    # Mostrar la imagen en una nueva ventana
                    self.ventana_imagen = QLabel()
                    pixmap = pixmap.scaled(800, 600, aspectRatioMode=1)
                    self.ventana_imagen.setPixmap(pixmap)
                    self.ventana_imagen.show()
                else:
                    QMessageBox.warning(self, "Error", f"No se pudo cargar la imagen. Código de error: {response.status_code}")
                    print(f"Respuesta del servidor: {response.text}")  # Debug
            else:
                QMessageBox.information(self, "Info", "Este pedido no tiene un plano adjunto")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar el plano: {str(e)}")
            print(f"Error completo: {str(e)}")  # Debug
    
    def guardar_cambios(self):
        try:
            # Validar el presupuesto
            presupuesto_texto = self.ui.lineEdit_11.text()
            try:
                presupuesto = float(presupuesto_texto) if presupuesto_texto else 0.0
            except ValueError:
                QMessageBox.warning(self, "Error", "El presupuesto debe ser un número válido")
                return

            # Verificar que el cliente no esté vacío
            if not self.ui.Cliente.text().strip():
                QMessageBox.warning(self, "Error", "El nombre del cliente no puede estar vacío")
                return

            # Preparar los datos
            datos = {
                'cliente_nombre': self.ui.Cliente.text().strip(),
                'estado': self.ui.comboBox.currentText(),
                'fecha_medicion': self.ui.dateEdit.date().toString("yyyy-MM-dd"),
                'fecha_llegada_materiales': self.ui.dateEdit_3.date().toString("yyyy-MM-dd"),
                'fecha_entrega': self.ui.dateEdit_2.date().toString("yyyy-MM-dd"),
                'presupuesto': presupuesto,
                'notas': self.ui.plainTextEdit.toPlainText()
            }

            # Si hay un plano temporal, abrir el archivo y mantenerlo abierto
            archivo_plano = None
            if self.plano_temp:
                try:
                    # Abrir el archivo
                    archivo_plano = open(self.plano_temp, 'rb')
                    # Crear un diccionario con el archivo
                    datos['files'] = {'plano': archivo_plano}
                    print(f"📁 Enviando archivo: {self.plano_temp}")  # Debug
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al abrir el archivo del plano: {str(e)}")
                    return

            try:
                # Si no hay pedido_id, es un nuevo pedido
                if not self.pedido_id:
                    resultado = ApiService.crear_pedido(datos)
                    if resultado:
                        QMessageBox.information(self, "Éxito", "Pedido creado correctamente")
                        self.pedido_actualizado.emit()
                        self.close()  # Cerrar la ventana después de crear
                    else:
                        QMessageBox.critical(self, "Error", "No se pudo crear el pedido. Verifica que estés autenticado y vuelve a intentarlo.")
                else:
                    # Actualizar pedido existente
                    resultado = ApiService.actualizar_pedido(self.pedido_id, datos)
                    if resultado:
                        QMessageBox.information(self, "Éxito", "Pedido actualizado correctamente")
                        self.pedido_actualizado.emit()
                        self.close()  # Cerrar la ventana después de actualizar
                    else:
                        QMessageBox.critical(self, "Error", "No se pudo actualizar el pedido. Verifica que estés autenticado y vuelve a intentarlo.")
            finally:
                # Asegurarse de cerrar el archivo después de la petición
                if archivo_plano:
                    archivo_plano.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar los cambios: {str(e)}")
            print(f"Error completo: {str(e)}")  # Debug

    def __del__(self):
        # Cerrar la conexión cuando se destruye el objeto
        if hasattr(self, 'conn') and self.conn:
            self.conn.close() 