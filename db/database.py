import sqlite3

class Database:
    def __init__(self, db_name="db/TallerCarpinteria.db"):
        self.db_name = db_name
    
    def connect(self):
        """Conectar a la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error as e:
            print(f"Error al conectar la base de datos: {e}")
            return None
    
    def crear_tablas(self):
        """Crear las tablas necesarias si no existen"""
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Crear tabla pedidos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS pedidos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cliente_nombre TEXT NOT NULL,
                        estado TEXT NOT NULL,
                        fecha_medicion TEXT,
                        presupuesto REAL,
                        fecha_llegada_materiales TEXT,
                        fecha_entrega TEXT,
                        ruta_plano TEXT,
                        notas TEXT
                    )
                """)
                
                # Insertar algunos datos de prueba
                cursor.execute("""
                    INSERT OR IGNORE INTO pedidos (
                        id, cliente_nombre, estado, fecha_medicion, 
                        presupuesto, fecha_llegada_materiales, fecha_entrega,
                        notas
                    ) VALUES 
                    (1, 'MAXI GRECO', 'Medicion', '2024-03-15', 
                     150000, '2024-03-20', '2024-04-01',
                     'Notas de ejemplo para el pedido')
                """)
                
                conn.commit()
                print("✅ Tablas creadas exitosamente")
            except sqlite3.Error as e:
                print(f"Error al crear las tablas: {e}")
            finally:
                conn.close()
    
    