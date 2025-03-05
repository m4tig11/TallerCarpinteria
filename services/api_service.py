import requests

class ApiService:
    BASE_URL = "http://localhost:8000/api"  # Ajusta esto según tu configuración

    @staticmethod
    def get_pedidos():
        try:
            response = requests.get(f"{ApiService.BASE_URL}/pedidos/")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error al obtener pedidos: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error en la conexión con la API: {e}")
            return []

    @staticmethod
    def get_pedido(pedido_id):
        try:
            response = requests.get(f"{ApiService.BASE_URL}/pedidos/{pedido_id}/")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error al obtener pedido: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error en la conexión con la API: {e}")
            return None

    @staticmethod
    def actualizar_pedido(pedido_id, datos):
        try:
            response = requests.put(
                f"{ApiService.BASE_URL}/pedidos/{pedido_id}/",
                json=datos
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Error al actualizar pedido: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error en la conexión con la API: {e}")
            return None

    @staticmethod
    def crear_pedido(datos):
        try:
            response = requests.post(
                f"{ApiService.BASE_URL}/pedidos/",
                json=datos
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Error al crear pedido: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error en la conexión con la API: {e}")
            return None 