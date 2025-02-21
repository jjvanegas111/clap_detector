import socket

# Configuración del servidor
HOST = "192.168.1.5"  # Escucha en todas las interfaces de red
PORT = 5001       # Puerto de comunicación

# Crear el socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"🔍 Servidor escuchando en {HOST}:{PORT}...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"📥 Conexión establecida con {client_address}")

    # Recibir datos de la ESP32
    data = client_socket.recv(1024).decode()
    print(f"🎤 Datos recibidos: {data}")

    # Aquí se procesaría el audio con la IA (por ahora solo respondemos "OK")
    response = "OK"
    
    client_socket.send(response.encode())  # Enviar respuesta a la ESP32
    print(f"📤 Respuesta enviada: {response}")

    client_socket.close()