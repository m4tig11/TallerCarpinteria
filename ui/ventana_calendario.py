from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QCalendarWidget,
    QListWidget,
    QFrame,
    QScrollArea
)
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QTextCharFormat

class Ui_CalendarioWindow:
    def setupUi(self, CalendarioWindow):
        CalendarioWindow.setObjectName("CalendarioWindow")
        CalendarioWindow.resize(1400, 900)
        CalendarioWindow.setMinimumSize(1400, 900)
        
        # Widget central
        self.centralwidget = QWidget(CalendarioWindow)
        CalendarioWindow.setCentralWidget(self.centralwidget)
        
        # Layout principal
        self.layout_principal = QHBoxLayout(self.centralwidget)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)
        
        # Panel lateral
        self.panel_lateral = QFrame()
        self.panel_lateral.setFixedWidth(300)
        self.panel_lateral.setStyleSheet("""
            QFrame {
                background-color: #1e272e;
                border: none;
            }
        """)
        
        self.layout_lateral = QVBoxLayout(self.panel_lateral)
        self.layout_lateral.setContentsMargins(25, 30, 25, 30)
        self.layout_lateral.setSpacing(20)
        
        # Logo o Icono
        self.logo = QtWidgets.QLabel()
        self.logo.setFixedSize(125, 125)
        pixmap = QPixmap("imagenes/logo/logo.png")
        pixmap = pixmap.scaled(125, 125, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setStyleSheet("""
            QLabel {
                border-radius: 40px;
                background-color: transparent;
            }
        """)
        self.layout_lateral.addWidget(self.logo, alignment=Qt.AlignCenter)
        
        # Título
        self.titulo = QLabel("Calendario")
        self.titulo.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.titulo.setStyleSheet("color: white; margin-bottom: 10px;")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.layout_lateral.addWidget(self.titulo)
        
        # Separador
        self.separador = QFrame()
        self.separador.setFrameShape(QFrame.HLine)
        self.separador.setStyleSheet("background-color: #34495e;")
        self.layout_lateral.addWidget(self.separador)
        
        # Botón de inicio con icono
        self.home = QPushButton(" Inicio")
        self.home.setFont(QFont("Segoe UI", 12))
        self.home.setStyleSheet("""
            QPushButton {
                background-color: #2e86de;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #54a0ff;
            }
        """)
        self.layout_lateral.addWidget(self.home)
        
        # Información del día
        self.info_dia = QLabel("Eventos del día")
        self.info_dia.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.info_dia.setStyleSheet("color: white; margin-top: 20px;")
        self.layout_lateral.addWidget(self.info_dia)
        
        # Lista de eventos con scroll
        self.scroll_eventos = QScrollArea()
        self.scroll_eventos.setWidgetResizable(True)
        self.scroll_eventos.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #2d3436;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #636e72;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # Widget contenedor para la lista de eventos
        self.contenedor_eventos = QWidget()
        self.layout_eventos = QVBoxLayout(self.contenedor_eventos)
        self.layout_eventos.setContentsMargins(0, 0, 0, 0)
        self.layout_eventos.setSpacing(10)
        
        self.listaEventos = QListWidget()
        self.listaEventos.setStyleSheet("""
            QListWidget {
                background-color: #2d3436;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                background-color: #34495e;
                color: white;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 5px;
            }
            QListWidget::item:selected {
                background-color: #2e86de;
            }
            QListWidget::item:hover {
                background-color: #3498db;
            }
        """)
        self.layout_eventos.addWidget(self.listaEventos)
        
        self.scroll_eventos.setWidget(self.contenedor_eventos)
        self.layout_lateral.addWidget(self.scroll_eventos)
        
        # Panel principal
        self.panel_principal = QWidget()
        self.panel_principal.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
            }
        """)
        
        self.layout_principal_panel = QVBoxLayout(self.panel_principal)
        self.layout_principal_panel.setContentsMargins(40, 40, 40, 40)
        self.layout_principal_panel.setSpacing(30)
        
        # Calendario
        self.calendario = QCalendarWidget()
        self.calendario.setMinimumSize(800, 600)
        self.calendario.setStyleSheet("""
            QCalendarWidget {
                background-color: white;
                border: none;
                border-radius: 15px;
            }
            QCalendarWidget QToolButton {
                color: #2d3436;
                background-color: transparent;
                font-size: 16px;
                icon-size: 24px;
                padding: 10px;
            }
            QCalendarWidget QMenu {
                background-color: white;
                border: 1px solid #dfe6e9;
            }
            QCalendarWidget QSpinBox {
                font-size: 16px;
                background-color: white;
                selection-background-color: #2e86de;
                selection-color: white;
            }
            QCalendarWidget QTableView {
                background-color: white;
                selection-background-color: #2e86de;
                selection-color: white;
                font-size: 14px;
                outline: 0px;
            }
            QCalendarWidget QTableView::item:hover {
                background-color: #f0f0f0;
            }
            QCalendarWidget QTableView::item:selected {
                background-color: #2e86de;
                color: white;
            }
            /* Estilo para los días de la semana */
            QCalendarWidget QTableView QHeaderView::section {
                background-color: #f5f6fa;
                color: #2d3436;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
                border: none;
            }
        """)
        self.calendario.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendario.setHorizontalHeaderFormat(QCalendarWidget.SingleLetterDayNames)
        self.calendario.setNavigationBarVisible(True)
        self.calendario.setGridVisible(True)
        
        # Configurar el formato de las celdas del calendario
        formato_medicion = QTextCharFormat()
        formato_medicion.setBackground(QColor("#2ecc71"))
        formato_medicion.setForeground(QColor("white"))
        
        formato_entrega = QTextCharFormat()
        formato_entrega.setBackground(QColor("#e74c3c"))
        formato_entrega.setForeground(QColor("white"))
        
        formato_materiales = QTextCharFormat()
        formato_materiales.setBackground(QColor("#f1c40f"))
        formato_materiales.setForeground(QColor("white"))
        
        self.layout_principal_panel.addWidget(self.calendario)
        
        # Agregar paneles al layout principal
        self.layout_principal.addWidget(self.panel_lateral)
        self.layout_principal.addWidget(self.panel_principal)

        self.retranslateUi(CalendarioWindow)
        QtCore.QMetaObject.connectSlotsByName(CalendarioWindow)
    
    def retranslateUi(self, CalendarioWindow):
        _translate = QtCore.QCoreApplication.translate
        CalendarioWindow.setWindowTitle(_translate("CalendarioWindow", "Calendario de Pedidos"))
        self.home.setText(_translate("CalendarioWindow", "Inicio"))
        self.titulo.setText(_translate("CalendarioWindow", "Calendario")) 