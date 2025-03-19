from PyQt5.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QScrollArea, 
    QLabel, 
    QPushButton,
    QFrame,
    QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from ui.Home import Ui_MainWindow
from db.database import Database
from services.api_service import ApiService
from controllers.pedido_controller import PedidoController
from controllers.calendario_controller import CalendarioController

class TarjetaPedido(QWidget):
    def __init__(self, pedido_data):
        super().__init__()
        
        # Configurar widget principal
        self.setFixedSize(280, 160)
        
        # Frame principal
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 280, 160)
        self.frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #E0E0E0;
            }
        """)
        
        # Layout principal
        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)
        
        # Layout superior (ID y Nombre)
        layout_superior = QHBoxLayout()
        
        # ID del pedido
        id_label = QLabel(f"#{pedido_data['id']}")
        id_label.setStyleSheet("""
            font-family: Segoe UI;
            font-size: 12px;
            color: #007AFF;
            background-color: #F0F7FF;
            padding: 4px 8px;
            border-radius: 8px;
        """)
        
        # Nombre del cliente
        nombre_label = QLabel(pedido_data['cliente_nombre'])
        nombre_label.setStyleSheet("""
            font-family: Segoe UI;
            font-weight: bold;
            font-size: 16px;
            color: #1A1A1A;
        """)
        
        layout_superior.addWidget(id_label)
        layout_superior.addWidget(nombre_label)
        layout_superior.addStretch()
        
        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setStyleSheet("background-color: #E0E0E0;")
        separador.setFixedHeight(1)
        
        # Layout para estado y fecha
        layout_info = QHBoxLayout()
        
        # Estado actual
        estado_label = QLabel(pedido_data['estado'])
        estado_label.setStyleSheet("""
            font-family: Segoe UI;
            font-size: 14px;
            color: #333333;
            background-color: #F5F5F5;
            padding: 5px 12px;
            border-radius: 12px;
        """)
        
        # Fecha de medición como fecha principal
        fecha_label = QLabel(pedido_data['fecha_medicion'])
        fecha_label.setStyleSheet("""
            font-family: Segoe UI;
            font-size: 14px;
            color: #666666;
        """)
        
        layout_info.addWidget(estado_label)
        layout_info.addWidget(fecha_label, alignment=Qt.AlignRight)
        
        # Botón Ver Detalles
        btn_detalles = QPushButton("Ver detalles")
        btn_detalles.setFixedSize(110, 32)
        btn_detalles.setCursor(Qt.PointingHandCursor)
        btn_detalles.setStyleSheet("""
            QPushButton {
                background-color: #2e86de;
                color: white;
                border-radius: 16px;
                font-family: Segoe UI;
                font-size: 13px;
                font-weight: bold;
                padding: 0 15px;
            }
            QPushButton:hover {
                background-color: #54a0ff;
            }
        """)
        btn_detalles.clicked.connect(lambda: self.abrir_detalles(pedido_data['id']))
        
        # Agregar todos los elementos al layout principal
        layout.addLayout(layout_superior)
        layout.addWidget(separador)
        layout.addLayout(layout_info)
        layout.addWidget(btn_detalles, alignment=Qt.AlignRight)
    
    def abrir_detalles(self, pedido_id):
        self.ventana_pedido = PedidoController(pedido_id)
        # Conectar la señal de actualización con el HomeController
        parent = self.window()
        if isinstance(parent, HomeController):
            self.ventana_pedido.pedido_actualizado.connect(parent.cargar_pedidos)
        self.ventana_pedido.show()

class HomeController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Conectar señales
        self.ui.btnNuevoPedido.clicked.connect(self.nuevo_pedido)
        self.ui.btnCalendario.clicked.connect(self.abrir_calendario)
        
        # Configurar scroll areas para cada columna
        self.scroll_solicitados = self.crear_scroll_area(self.ui.container_solicitados)
        self.scroll_proceso = self.crear_scroll_area(self.ui.container_proceso)
        self.scroll_entregar = self.crear_scroll_area(self.ui.container_entregar)
        
        # Crear layouts para cada scroll area
        self.layout_solicitados = QVBoxLayout(self.scroll_solicitados.widget())
        self.layout_proceso = QVBoxLayout(self.scroll_proceso.widget())
        self.layout_entregar = QVBoxLayout(self.scroll_entregar.widget())
        
        # Configurar layouts
        for layout in [self.layout_solicitados, self.layout_proceso, self.layout_entregar]:
            layout.setSpacing(15)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setAlignment(Qt.AlignTop)
        
        # Cargar pedidos
        self.cargar_pedidos()
    
    def crear_scroll_area(self, parent):
        scroll = QScrollArea(parent)
        scroll.setGeometry(0, 0, parent.width(), parent.height())
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # Crear y configurar widget contenedor
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        scroll.setWidget(content)
        
        return scroll
    
    def cargar_pedidos(self):
        try:
            pedidos = ApiService.get_pedidos()
            
            # Limpiar los contenedores existentes
            for layout in [self.layout_solicitados, self.layout_proceso, self.layout_entregar]:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
            
            # Distribuir los pedidos según su estado
            for pedido in pedidos:
                tarjeta = TarjetaPedido(pedido)
                if pedido['estado'] == 'Solicitado':
                    self.layout_solicitados.addWidget(tarjeta)
                elif pedido['estado'] in ['En proceso', 'Materiales']:
                    self.layout_proceso.addWidget(tarjeta)
                elif pedido['estado'] in ['Para entregar', 'Terminado']:
                    self.layout_entregar.addWidget(tarjeta)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los pedidos: {str(e)}")
    
    def nuevo_pedido(self):
        self.pedido = PedidoController()
        self.pedido.show()
        
    
    def abrir_calendario(self):
        self.calendario = CalendarioController()
        self.calendario.show()
        self.close()