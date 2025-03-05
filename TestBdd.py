import requests

url = "http://127.0.0.1:8000/api/pedidos/"
response = requests.get(url)

print(f"Status Code: {response.status_code}")  # Verifica el código de estado

if response.status_code == 200:  # Verifica si la solicitud fue exitosa
    try:
        data = response.json()
        print(data)
    except requests.exceptions.JSONDecodeError:
        print("Error: La respuesta no es un JSON válido.")
else:
    print(f"Error: Código de estado {response.status_code}")
    print("Contenido de la respuesta:", response.text)  # Muestra el contenido para analizar el problema
