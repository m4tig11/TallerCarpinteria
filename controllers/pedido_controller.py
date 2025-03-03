from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap
from ui.ventana_pedido import Ui_MainWindow
from db.database import Database
import os
import shutil

class PedidoController(QMainWindow):
    def __init__(self, pedido_id=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pedido_id = pedido_id
        
        # Crear directorio para imágenes si no existe
        self.img_dir = "imagenes/planos"
        os.makedirs(self.img_dir, exist_ok=True)
        
        # Conectar botones
        self.ui.pushButton_3.clicked.connect(self.guardar_cambios)
        self.ui.pushButton.clicked.connect(self.ver_plano)      # Botón Ver
        self.ui.pushButton_2.clicked.connect(self.adjuntar_plano)  # Botón Adjuntar
        
        self.inicializar_db()
        
        # Si hay un ID de pedido, cargar los datos
        if self.pedido_id:
            self.cargar_pedido()
    
    def inicializar_db(self):
        self.db = Database()
        self.conn = self.db.connect()

        if self.conn:
            print("✅ Conexión exitosa a la base de datos")
        else:
            print("❌ No se pudo conectar a la base de datos")
    
    def cargar_pedido(self):
        if not self.conn:
            print("Error: No hay conexión a la base de datos")
            return
            
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT cliente_nombre, estado, fecha_medicion, presupuesto, 
                   fecha_llegada_materiales, fecha_entrega, notas
            FROM pedidos 
            WHERE id = ?
        """, (self.pedido_id,))
        
        resultado = cursor.fetchone()
        
        if resultado:
            # Desempaquetar los resultados
            cliente, etapa, fecha_medicion, presupuesto, fecha_materiales, fecha_entrega, notas = resultado
            
            # Establecer los valores en los widgets
            self.ui.Cliente.setText(cliente)
            self.ui.comboBox.setCurrentText(etapa)
            
            # Convertir strings de fecha a QDate y establecerlos
            self.ui.dateEdit.setDate(QDate.fromString(fecha_medicion, "yyyy-MM-dd"))
            self.ui.dateEdit_3.setDate(QDate.fromString(fecha_materiales, "yyyy-MM-dd"))
            self.ui.dateEdit_2.setDate(QDate.fromString(fecha_entrega, "yyyy-MM-dd"))
            
            self.ui.lineEdit_11.setText(str(presupuesto))
            
            # Establecer las notas
            if notas:
                self.ui.plainTextEdit.setPlainText(notas)
        else:
            print(f"No se encontró el pedido con ID: {self.pedido_id}")

    def guardar_cambios(self):
        # Obtener los valores de los campos
        cliente = self.ui.Cliente.text()
        etapa = self.ui.comboBox.currentText()
        
        # Obtener las fechas de los QDateEdit
        fecha_medicion = self.ui.dateEdit.date().toString("yyyy-MM-dd")
        fecha_materiales = self.ui.dateEdit_3.date().toString("yyyy-MM-dd")
        fecha_entrega = self.ui.dateEdit_2.date().toString("yyyy-MM-dd")
        
        # Obtener el presupuesto y las notas
        presupuesto = self.ui.lineEdit_11.text()
        notas = self.ui.plainTextEdit.toPlainText()
        
        try:
            cursor = self.conn.cursor()
            
            if self.pedido_id:  # Actualizar pedido existente
                cursor.execute("""
                    UPDATE pedidos 
                    SET cliente_nombre = ?, 
                        estado = ?,
                        fecha_medicion = ?,
                        presupuesto = ?,
                        fecha_llegada_materiales = ?,
                        fecha_entrega = ?,
                        notas = ?
                    WHERE id = ?
                """, (cliente, etapa, fecha_medicion, presupuesto, 
                      fecha_materiales, fecha_entrega, notas, self.pedido_id))
                
                self.conn.commit()
                print(f"✅ Pedido {self.pedido_id} actualizado exitosamente")
                
            else:  # Crear nuevo pedido
                cursor.execute("""
                    INSERT INTO pedidos (
                        cliente_nombre, estado, fecha_medicion, 
                        presupuesto, fecha_llegada_materiales, fecha_entrega,
                        notas
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (cliente, etapa, fecha_medicion, presupuesto, 
                      fecha_materiales, fecha_entrega, notas))
                
                self.conn.commit()
                self.pedido_id = cursor.lastrowid
                print(f"✅ Nuevo pedido creado con ID: {self.pedido_id}")
            
        except Exception as e:
            print(f"Error al guardar los cambios: {e}")
            self.conn.rollback()

    def adjuntar_plano(self):
        # Abrir diálogo para seleccionar archivo
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Plano",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp);;Todos los archivos (*.*)"
        )
        
        if archivo:
            # Crear nombre de archivo basado en el ID del pedido
            extension = os.path.splitext(archivo)[1]
            nuevo_nombre = f"plano_pedido_{self.pedido_id}{extension}"
            ruta_destino = os.path.join(self.img_dir, nuevo_nombre)
            
            # Copiar archivo a la carpeta de imágenes
            try:
                shutil.copy2(archivo, ruta_destino)
                print(f"✅ Plano guardado como: {nuevo_nombre}")
                
                # Guardar ruta en la base de datos
                cursor = self.conn.cursor()
                cursor.execute("""
                    UPDATE pedidos 
                    SET ruta_plano = ? 
                    WHERE id = ?
                """, (nuevo_nombre, self.pedido_id))
                self.conn.commit()
                
            except Exception as e:
                print(f"Error al guardar el plano: {e}")
    
    def ver_plano(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ruta_plano FROM pedidos WHERE id = ?", (self.pedido_id,))
            resultado = cursor.fetchone()
            
            if resultado and resultado[0]:
                ruta_plano = os.path.join(self.img_dir, resultado[0])
                if os.path.exists(ruta_plano):
                    # Crear una nueva ventana para mostrar la imagen
                    self.ventana_imagen = QLabel()
                    pixmap = QPixmap(ruta_plano)
                    # Escalar la imagen manteniendo proporción
                    pixmap = pixmap.scaled(800, 600, aspectRatioMode=1)
                    self.ventana_imagen.setPixmap(pixmap)
                    self.ventana_imagen.show()
                else:
                    print("No se encontró el archivo del plano")
            else:
                print("Este pedido no tiene un plano adjunto")
                
        except Exception as e:
            print(f"Error al mostrar el plano: {e}")

    def __del__(self):
        # Cerrar la conexión cuando se destruye el objeto
        if hasattr(self, 'conn') and self.conn:
            self.conn.close() 