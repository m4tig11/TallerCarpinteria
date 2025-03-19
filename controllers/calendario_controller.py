from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QTextCharFormat, QColor
from ui.ventana_calendario import Ui_CalendarioWindow
from services.api_service import ApiService
from datetime import datetime

class CalendarioController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_CalendarioWindow()
        self.ui.setupUi(self)
        
        # Conectar señales
        self.ui.home.clicked.connect(self.volver_home)
        self.ui.calendario.clicked.connect(self.fecha_seleccionada)
        self.ui.calendario.selectionChanged.connect(self.fecha_seleccionada)
        
        # Formatos para diferentes tipos de eventos
        self.formato_medicion = QTextCharFormat()
        self.formato_medicion.setBackground(QColor("#2ecc71"))
        self.formato_medicion.setForeground(QColor("white"))
        
        self.formato_entrega = QTextCharFormat()
        self.formato_entrega.setBackground(QColor("#e74c3c"))
        self.formato_entrega.setForeground(QColor("white"))
        
        self.formato_materiales = QTextCharFormat()
        self.formato_materiales.setBackground(QColor("#f1c40f"))
        self.formato_materiales.setForeground(QColor("white"))
        
        # Cargar eventos
        self.cargar_eventos()
    
    def cargar_eventos(self):
        try:
            # Obtener todos los pedidos
            pedidos = ApiService.get_pedidos()
            
            # Limpiar formatos existentes
            formato_default = QTextCharFormat()
            for fecha in self.ui.calendario.dateTextFormat():
                self.ui.calendario.setDateTextFormat(fecha, formato_default)
            
            # Procesar cada pedido
            for pedido in pedidos:
                # Marcar fechas importantes con diferentes colores
                if pedido['fecha_medicion']:
                    try:
                        fecha = datetime.strptime(pedido['fecha_medicion'], "%Y-%m-%d")
                        qfecha = QDate(fecha.year, fecha.month, fecha.day)
                        self.ui.calendario.setDateTextFormat(qfecha, self.formato_medicion)
                    except ValueError:
                        continue
                
                if pedido['fecha_llegada_materiales']:
                    try:
                        fecha = datetime.strptime(pedido['fecha_llegada_materiales'], "%Y-%m-%d")
                        qfecha = QDate(fecha.year, fecha.month, fecha.day)
                        self.ui.calendario.setDateTextFormat(qfecha, self.formato_materiales)
                    except ValueError:
                        continue
                
                if pedido['fecha_entrega']:
                    try:
                        fecha = datetime.strptime(pedido['fecha_entrega'], "%Y-%m-%d")
                        qfecha = QDate(fecha.year, fecha.month, fecha.day)
                        self.ui.calendario.setDateTextFormat(qfecha, self.formato_entrega)
                    except ValueError:
                        continue
            
            # Mostrar eventos del día actual
            self.fecha_seleccionada()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los eventos: {str(e)}")
    
    def fecha_seleccionada(self):
        # Obtener la fecha seleccionada
        fecha = self.ui.calendario.selectedDate()
        fecha_str = fecha.toString("yyyy-MM-dd")
        
        # Limpiar lista de eventos
        self.ui.listaEventos.clear()
        
        try:
            pedidos = ApiService.get_pedidos()
            eventos_del_dia = []
            
            for pedido in pedidos:
                # Verificar medición
                if pedido['fecha_medicion'] == fecha_str:
                    eventos_del_dia.append({
                        'tipo': 'Medición',
                        'color': '#2ecc71',
                        'pedido': pedido
                    })
                
                # Verificar llegada de materiales
                if pedido['fecha_llegada_materiales'] == fecha_str:
                    eventos_del_dia.append({
                        'tipo': 'Llegada de Materiales',
                        'color': '#f1c40f',
                        'pedido': pedido
                    })
                
                # Verificar entrega
                if pedido['fecha_entrega'] == fecha_str:
                    eventos_del_dia.append({
                        'tipo': 'Entrega',
                        'color': '#e74c3c',
                        'pedido': pedido
                    })
            
            # Mostrar eventos en la lista
            for evento in eventos_del_dia:
                item_text = f"{evento['tipo']}\nPedido #{evento['pedido']['id']}\n{evento['pedido']['cliente_nombre']}"
                self.ui.listaEventos.addItem(item_text)
                ultimo_item = self.ui.listaEventos.item(self.ui.listaEventos.count() - 1)
                ultimo_item.setToolTip(f"Haga clic para ver más detalles del pedido #{evento['pedido']['id']}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al filtrar eventos: {str(e)}")
    
    def volver_home(self):
        from controllers.home_controller import HomeController
        self.home_window = HomeController()
        self.home_window.show()
        self.close() 