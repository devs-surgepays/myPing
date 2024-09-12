import json
import time
from ping3 import ping
import schedule
import http.server
import socketserver

# Lista de direcciones IP o DNS para hacer ping
hosts = ["8.8.8.8", "1.1.1.1", "google.com", "3.225.217.176"]

# Ruta del archivo JSON
json_file = "monitoring_data.json"

# Diccionario para almacenar los resultados
results = {host: [] for host in hosts}

# Función para hacer ping y guardar los resultados en un archivo JSON
def ping_hosts():
    data = {}
    for host in hosts:
        response_time = ping(host, timeout=2)  # Timeout de 2 segundos
        if response_time is None:
            response_time = "Timeout"  # Manejar pérdida de paquetes
        else:
            response_time = round(response_time * 1000, 2)  # Convertir a milisegundos
        
        data[host] = response_time
        print(f"Ping to {host}: {response_time} ms")

    # Guardar los resultados en un archivo JSON
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

# Configurar para hacer ping cada 0.52 segundos
schedule.every(1.10).seconds.do(ping_hosts)

# Iniciar el servidor HTTP en el puerto 8000
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

# Ejecutar el ping y el servidor
if __name__ == "__main__":
    # Hilo separado para el servidor
    import threading
    threading.Thread(target=start_server).start()

    # Correr el programa continuamente
    while True:
        schedule.run_pending()
        time.sleep(0.01)
