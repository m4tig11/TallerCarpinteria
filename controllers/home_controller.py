from PyQt5.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QScrollArea, 
    QLabel, 
    QPushButton,
    QFrame
)
from PyQt5.QtCore import Qt
from ui.Home import Ui_MainWindow
from db.database import Database
from services.api_service import ApiService

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
            font-family: Roboto;
            font-size: 12px;
            color: #007AFF;
            background-color: #F0F7FF;
            padding: 4px 8px;
            border-radius: 8px;
        """)
        
        # Nombre del cliente
        nombre_label = QLabel(pedido_data['cliente_nombre'])
        nombre_label.setStyleSheet("""
            font-family: Roboto;
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
        
        # Estado actual (antes era etapa)
        etapa_label = QLabel(pedido_data['estado'])
        etapa_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 14px;
            color: #333333;
            background-color: #F5F5F5;
            padding: 5px 12px;
            border-radius: 12px;
        """)
        
        # Fecha de medición como fecha principal
        fecha_label = QLabel(pedido_data['fecha_medicion'])
        fecha_label.setStyleSheet("""
            font-family: Roboto;
            font-size: 14px;
            color: #666666;
        """)
        
        layout_info.addWidget(etapa_label)
        layout_info.addWidget(fecha_label, alignment=Qt.AlignRight)
        
        # Botón Ver Detalles
        btn_detalles = QPushButton("Ver detalles")
        btn_detalles.setFixedSize(110, 32)
        btn_detalles.setCursor(Qt.PointingHandCursor)
        btn_detalles.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border-radius: 16px;
                font-family: Roboto;
                font-size: 13px;
                font-weight: bold;
                padding: 0 15px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        btn_detalles.clicked.connect(lambda: self.abrir_detalles(pedido_data['id']))
        
        # Agregar todos los elementos al layout principal
        layout.addLayout(layout_superior)
        layout.addWidget(separador)
        layout.addLayout(layout_info)
        layout.addWidget(btn_detalles, alignment=Qt.AlignRight)
    
    def abrir_detalles(self, pedido_id):
        from controllers.pedido_controller import PedidoController
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
        
        # Conectar el botón Nuevo Pedido
        self.ui.btnNuevoPedido.clicked.connect(self.nuevo_pedido)
        
        # Crear contenedores para cada columna
        self.container_solicitados = QWidget(self.ui.pantallaHome)
        self.container_proceso = QWidget(self.ui.pantallaHome)
        self.container_entregar = QWidget(self.ui.pantallaHome)
        
        # Establecer geometría
        self.container_solicitados.setGeometry(50, 140, 300, self.ui.pantallaHome.height() - 160)
        self.container_proceso.setGeometry(380, 140, 300, self.ui.pantallaHome.height() - 160)
        self.container_entregar.setGeometry(710, 140, 300, self.ui.pantallaHome.height() - 160)
        
        # Configurar scroll areas
        self.scroll_solicitados = self.crear_scroll_area(self.container_solicitados)
        self.scroll_proceso = self.crear_scroll_area(self.container_proceso)
        self.scroll_entregar = self.crear_scroll_area(self.container_entregar)
        
        # Crear layouts
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
        scroll.setGeometry(0, 0, 300, parent.height())
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # Crear y configurar widget contenedor
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        scroll.setWidget(content)
        
        return scroll
    
    def cargar_pedidos(self):
        # Obtener pedidos desde la API
        pedidos = ApiService.get_pedidos()
        
        # Limpiar layouts existentes
        self.limpiar_layouts()
        
        # Crear tarjetas
        for pedido in pedidos:
            tarjeta = TarjetaPedido(pedido)
            
            # Distribuir según etapa
            estado = pedido['estado'].lower()
            if estado in ['medicion', 'solicitud', 'pendiente']:
                print("Agregando a Solicitados")
                self.layout_solicitados.addWidget(tarjeta)
            elif estado in ['en proceso', 'proceso', 'fabricacion', 'materiales']:
                print("Agregando a En proceso")
                self.layout_proceso.addWidget(tarjeta)
            elif estado in ['entrega', 'para entregar', 'finalizado']:
                print("Agregando a Para entregar")
                self.layout_entregar.addWidget(tarjeta)
            else:
                print(f"Estado no reconocido: {estado}")
                self.layout_proceso.addWidget(tarjeta)
        
        # Agregar espacio al final de cada columna
        self.layout_solicitados.addStretch()
        self.layout_proceso.addStretch()
        self.layout_entregar.addStretch()
    
    def limpiar_layouts(self):
        for layout in [self.layout_solicitados, self.layout_proceso, self.layout_entregar]:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
    
    def nuevo_pedido(self):
        from controllers.pedido_controller import PedidoController
        self.ventana_pedido = PedidoController()  # Sin ID para nuevo pedido
        # Conectar la señal de actualización
        self.ventana_pedido.pedido_actualizado.connect(self.cargar_pedidos)
        self.ventana_pedido.show()