import socket  

HOST = "192.168.1.5"  # Reemplázalo con la IP de tu MacBook
PORT = 5001  # Asegúrate de usar el mismo puerto que configuraste en el servidor  

# Crear socket y conectar al servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Enviar un mensaje de prueba
client_socket.sendall(b"TEST AUDIO DATA")

# Recibir la respuesta
response = client_socket.recv(1024)
print(f"Respuesta del servidor: {response.decode()}")

client_socket.close()