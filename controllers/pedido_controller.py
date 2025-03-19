from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel, QMessageBox, QPushButton, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
from ui.ventana_pedido import Ui_MainWindow
from services.api_service import ApiService
import os
import requests
from io import BytesIO
from datetime import datetime

class PedidoController(QMainWindow):
    # Agregar señal de actualización
    pedido_actualizado = pyqtSignal()
    
    def __init__(self, pedido_id=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pedido_id = pedido_id
        self.plano_temp = None  # Para almacenar temporalmente la imagen seleccionada
        
        # Crear botones para planos
        self.layout_planos = QHBoxLayout()
        
        # Botón Ver Plano
        self.btn_ver_plano = QPushButton("Ver Plano")
        self.btn_ver_plano.setFont(QFont("Segoe UI", 12))
        self.btn_ver_plano.setStyleSheet("""
            QPushButton {
                background-color: #2e86de;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #54a0ff;
            }
        """)
        
        # Botón Adjuntar Plano
        self.btn_adjuntar_plano = QPushButton("Adjuntar Plano")
        self.btn_adjuntar_plano.setFont(QFont("Segoe UI", 12))
        self.btn_adjuntar_plano.setStyleSheet("""
            QPushButton {
                background-color: #2e86de;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #54a0ff;
            }
        """)
        
        # Agregar botones al layout
        self.layout_planos.addWidget(self.btn_ver_plano)
        self.layout_planos.addWidget(self.btn_adjuntar_plano)
        
        # Agregar layout de planos al contenido principal antes de los botones de acción
        self.ui.contenido.layout().addLayout(self.layout_planos)
        
        # Conectar señales
        self.ui.btn_guardar.clicked.connect(self.guardar_cambios)
        self.ui.btn_cancelar.clicked.connect(self.close)
        self.btn_ver_plano.clicked.connect(self.ver_plano)
        self.btn_adjuntar_plano.clicked.connect(self.adjuntar_plano)
        
        # Configurar fechas por defecto
        fecha_actual = QDate.currentDate()
        self.ui.input_fecha_medicion.setDate(fecha_actual)
        self.ui.input_fecha_entrega.setDate(fecha_actual)
        self.ui.input_fecha_materiales.setDate(fecha_actual)
        
        if self.pedido_id:
            # Es modo edición
            self.ui.titulo_pedido.setText(f"Editar Pedido #{pedido_id}")
            self.ui.estado_pedido.show()
            self.btn_ver_plano.show()
            self.btn_adjuntar_plano.show()
            # Cargar datos del pedido
            self.cargar_pedido(pedido_id)
        else:
            # Es nuevo pedido
            self.ui.titulo_pedido.setText("Nuevo Pedido")
            self.ui.estado_pedido.hide()
            self.btn_ver_plano.hide()
            self.btn_adjuntar_plano.hide()
    
    def cargar_pedido(self, pedido_id):
        try:
            # Obtener datos del pedido
            pedido = ApiService.get_pedido(pedido_id)
            if not pedido:
                QMessageBox.critical(self, "Error", "No se pudo cargar el pedido")
                self.close()
                return
            
            print(f"Datos del pedido cargado: {pedido}")  # Debug
            
            # Cargar datos en los campos
            self.ui.input_cliente.setText(str(pedido.get('cliente_nombre', '')))
            self.ui.input_presupuesto.setText(str(pedido.get('presupuesto', '0')))
            self.ui.input_notas.setText(str(pedido.get('notas', '')))
            
            # Cargar fechas
            try:
                if pedido.get('fecha_medicion'):
                    fecha = datetime.strptime(pedido['fecha_medicion'], "%Y-%m-%d")
                    self.ui.input_fecha_medicion.setDate(QDate(fecha.year, fecha.month, fecha.day))
                
                if pedido.get('fecha_entrega'):
                    fecha = datetime.strptime(pedido['fecha_entrega'], "%Y-%m-%d")
                    self.ui.input_fecha_entrega.setDate(QDate(fecha.year, fecha.month, fecha.day))
                
                if pedido.get('fecha_llegada_materiales'):
                    fecha = datetime.strptime(pedido['fecha_llegada_materiales'], "%Y-%m-%d")
                    self.ui.input_fecha_materiales.setDate(QDate(fecha.year, fecha.month, fecha.day))
            except ValueError as e:
                print(f"Error al procesar fechas: {e}")  # Debug
            
            # Establecer estado actual
            if pedido.get('estado'):
                index = self.ui.estado_pedido.findText(pedido['estado'])
                if index >= 0:
                    self.ui.estado_pedido.setCurrentIndex(index)
            
        except Exception as e:
            print(f"Error al cargar pedido: {str(e)}")  # Debug
            QMessageBox.critical(self, "Error", f"Error al cargar el pedido: {str(e)}")
    
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
        if not self.pedido_id:
            QMessageBox.information(self, "Info", "Primero debe guardar el pedido para poder ver el plano")
            return
            
        try:
            pedido = ApiService.get_pedido(self.pedido_id)
            
            if pedido and pedido.get('plano'):
                # Obtener la URL completa de la imagen
                imagen_url = pedido['plano']
                print(f"Intentando cargar imagen desde: {imagen_url}")  # Debug
                
                # Hacer la petición para obtener la imagen
                headers = ApiService.get_auth_headers()
                response = requests.get(imagen_url, headers=headers)
                
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
            else:
                QMessageBox.information(self, "Info", "Este pedido no tiene un plano adjunto")
                
        except Exception as e:
            print(f"Error al mostrar plano: {str(e)}")  # Debug
            QMessageBox.critical(self, "Error", f"Error al mostrar el plano: {str(e)}")
    
    def guardar_cambios(self):
        datos_pedido = None
        try:
            # Validar campos requeridos
            if not self.ui.input_cliente.text().strip():
                QMessageBox.warning(self, "Error", "El nombre del cliente es obligatorio")
                return
            
            # Validar que el presupuesto sea un número
            try:
                presupuesto = float(self.ui.input_presupuesto.text().strip() or "0")
            except ValueError:
                QMessageBox.warning(self, "Error", "El presupuesto debe ser un número válido")
                return
            
            # Recopilar datos del formulario
            datos_pedido = {
                'cliente_nombre': self.ui.input_cliente.text().strip(),
                'fecha_medicion': self.ui.input_fecha_medicion.date().toString("yyyy-MM-dd"),
                'fecha_entrega': self.ui.input_fecha_entrega.date().toString("yyyy-MM-dd"),
                'fecha_llegada_materiales': self.ui.input_fecha_materiales.date().toString("yyyy-MM-dd"),
                'presupuesto': str(presupuesto),
                'notas': self.ui.input_notas.toPlainText().strip() or "Sin notas"
            }
            
            # Si hay un plano seleccionado, agregarlo a los datos
            if self.plano_temp:
                datos_pedido['files'] = {'plano': open(self.plano_temp, 'rb')}
            
            # Si es edición, incluir el estado
            if self.pedido_id:
                datos_pedido['estado'] = self.ui.estado_pedido.currentText()
                # Actualizar pedido existente
                resultado = ApiService.actualizar_pedido(self.pedido_id, datos_pedido)
                if not resultado:
                    raise Exception("Error al actualizar el pedido. Por favor, verifica tu conexión e inténtalo de nuevo.")
                mensaje = "Pedido actualizado correctamente"
            else:
                # Crear nuevo pedido
                datos_pedido['estado'] = 'Solicitado'  # Estado por defecto para nuevos pedidos
                resultado = ApiService.crear_pedido(datos_pedido)
                if not resultado:
                    raise Exception("Error al crear el pedido. Por favor, verifica tu conexión e inténtalo de nuevo.")
                mensaje = "Pedido creado correctamente"
            
            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Éxito", mensaje)
            
            # Emitir señal de actualización
            self.pedido_actualizado.emit()
            
            # Cerrar ventana solo si la operación fue exitosa
            self.close()
            
        except Exception as e:
            print(f"Error al guardar pedido: {str(e)}")  # Debug
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo guardar el pedido. Verifica tu conexión y que hayas iniciado sesión correctamente."
            )
            
        finally:
            # Cerrar el archivo si fue abierto
            if datos_pedido and 'files' in datos_pedido:
                try:
                    datos_pedido['files']['plano'].close()
                except:
                    pass