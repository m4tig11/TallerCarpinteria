import requests

class ApiService:
    BASE_URL = "http://localhost:8000/api"
    BASE_URL = "http://127.0.0.1:8000/api"
    ACCESS_TOKEN = None  # Guardar el token de acceso
    REFRESH_TOKEN = None  # Guardar el token de refresco

    @staticmethod
    def login(username, password):
        url = f"{ApiService.BASE_URL}/token/"
        data = {"username": username, "password": password}

        try:
            response = requests.post(url, json=data)
            print("Código de respuesta:", response.status_code)
            print("Respuesta del servidor:", response.text)  

            if response.status_code == 200:
                tokens = response.json()
                ApiService.ACCESS_TOKEN = tokens.get("access")
                ApiService.REFRESH_TOKEN = tokens.get("refresh")

                if ApiService.ACCESS_TOKEN and ApiService.REFRESH_TOKEN:
                    print("Inicio de sesión exitoso. Token guardado.")
                    return ApiService.ACCESS_TOKEN
                else:
                    print("No se recibió un token válido.")
                    return None
            else:
                print(f"Error al iniciar sesión: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error en la conexión con la API: {e}")
            return None

    @staticmethod
    def get_auth_headers():
        if ApiService.ACCESS_TOKEN is None:
            print("⚠️ No hay token disponible. Inicia sesión.")
            return {}

        return {'Authorization': f'Bearer {ApiService.ACCESS_TOKEN}'}

    @staticmethod
    def refresh_token():
        if ApiService.REFRESH_TOKEN is None:
            print("No hay token de refresco. Debes iniciar sesión nuevamente.")
            return None

        try:
            response = requests.post(
                f"{ApiService.BASE_URL}/token/refresh/",
                json={"refresh": ApiService.REFRESH_TOKEN}
            )

            if response.status_code == 200:
                data = response.json()
                ApiService.ACCESS_TOKEN = data.get("access")

                if ApiService.ACCESS_TOKEN:
                    print("🔄 Token refrescado correctamente.")
                    return ApiService.ACCESS_TOKEN
                else:
                    print("No se recibió un nuevo access token.")
                    return None
            else:
                print(f"Error al refrescar token: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error en la conexión con la API: {e}")
            return None

    @staticmethod
    def get_pedidos():
        try:
            headers = ApiService.get_auth_headers()
            response = requests.get(f"{ApiService.BASE_URL}/pedidos/", headers=headers)

            if response.status_code == 401:  # Token expirado
                print("⏳ Token expirado. Intentando refrescar el token...")
                new_token = ApiService.refresh_token()

                if new_token:
                    headers = ApiService.get_auth_headers()
                    response = requests.get(f"{ApiService.BASE_URL}/pedidos/", headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error al obtener pedidos: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error en la conexión con la API: {e}")
            return []


    @staticmethod
    def save_token(token):
        # Aquí se guarda el token, por ejemplo, en el almacenamiento local o en cookies
        # En este caso, lo guardamos en una variable (simulación)
        print("Token guardado:", token)
        # localStorage.setItem('token', token) o cookies.set('token', token)

    

    @staticmethod
    def get_pedido(pedido_id):
        try:
            headers = ApiService.get_auth_headers()  # Incluir el token en los headers
            response = requests.get(f"{ApiService.BASE_URL}/pedidos/{pedido_id}/", headers=headers)
            if response.status_code == 200:
                return response.json()  # Devuelve el pedido solicitado
            else:
                print(f"Error al obtener pedido: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error en la conexión con la API: {e}")
            return None

    @staticmethod
    def actualizar_pedido(pedido_id, datos):
        try:
            # Verificar si tenemos un token válido
            if not ApiService.ACCESS_TOKEN:
                print("❌ No hay token de acceso. Debes iniciar sesión primero.")
                return None

            headers = ApiService.get_auth_headers()
            print(f"🔑 Headers de autenticación: {headers}")  # Debug
            
            # Si hay archivos (como el plano), usar data en lugar de json
            if 'files' in datos:
                files = datos.pop('files')
                response = requests.patch(
                f"{ApiService.BASE_URL}/pedidos/{pedido_id}/",
                data=datos,
                files=files,
                headers=headers
            )

            else:
                print(f"📦 Enviando datos: {datos}")  # Debug
                response = requests.put(
                    f"{ApiService.BASE_URL}/pedidos/{pedido_id}/",
                    json=datos,
                    headers=headers
                )
            
            print(f"📡 Código de respuesta: {response.status_code}")  # Debug
            print(f"📥 Respuesta del servidor: {response.text}")  # Debug
            
            # Si el token expiró, intentar refrescarlo y reintentar la petición
            if response.status_code == 401:
                print("⏳ Token expirado. Intentando refrescar el token...")
                new_token = ApiService.refresh_token()
                
                if new_token:
                    headers = ApiService.get_auth_headers()
                    print(f"🔄 Nuevos headers después del refresh: {headers}")  # Debug
                    
                    if 'files' in datos:
                        response = requests.put(
                            f"{ApiService.BASE_URL}/pedidos/{pedido_id}/",
                            data=datos,
                            files=files,
                            headers=headers
                        )
                    else:
                        response = requests.put(
                            f"{ApiService.BASE_URL}/pedidos/{pedido_id}/",
                            json=datos,
                            headers=headers
                        )
                    
                    print(f"📡 Código de respuesta después del refresh: {response.status_code}")  # Debug
                    print(f"📥 Respuesta del servidor después del refresh: {response.text}")  # Debug
                else:
                    print("❌ No se pudo refrescar el token. Debes iniciar sesión nuevamente.")
                    return None
            
            if response.status_code in [200, 201]:
                print("✅ Pedido actualizado correctamente")
                return response.json()
            else:
                print(f"❌ Error al actualizar pedido: {response.status_code}")
                print(f"📥 Respuesta del servidor: {response.text}")
                return None
            
        except Exception as e:
            print(f"❌ Error en la conexión con la API: {e}")
            return None

    @staticmethod
    def crear_pedido(datos):
        try:
            headers = ApiService.get_auth_headers()
            
            # Si hay archivos (como el plano), usar data en lugar de json
            if 'files' in datos:
                files = datos.pop('files')
                response = requests.post(
                    f"{ApiService.BASE_URL}/pedidos/",
                    data=datos,
                    files=files,
                    headers=headers
                )
            else:
                response = requests.post(
                    f"{ApiService.BASE_URL}/pedidos/",
                    json=datos,
                    headers=headers
                )
            
            # Si el token expiró, intentar refrescarlo y reintentar la petición
            if response.status_code == 401:
                print("⏳ Token expirado. Intentando refrescar el token...")
                new_token = ApiService.refresh_token()
                
                if new_token:
                    headers = ApiService.get_auth_headers()
                    if 'files' in datos:
                        response = requests.post(
                            f"{ApiService.BASE_URL}/pedidos/",
                            data=datos,
                            files=files,
                            headers=headers
                        )
                    else:
                        response = requests.post(
                            f"{ApiService.BASE_URL}/pedidos/",
                            json=datos,
                            headers=headers
                        )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Error al crear pedido: {response.status_code}")
                print(f"Respuesta del servidor: {response.text}")
                return None
            
        except Exception as e:
            print(f"Error en la conexión con la API: {e}")
            return None