import requests

url = 'http://127.0.0.1:8000/api/pedidos/'
response = requests.get(url)
data = response.json()

# Aquí puedes procesar los datos recibidos
print(data)
