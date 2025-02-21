import socket
import numpy as np
import librosa
import tensorflow as tf

# Configuración del servidor
HOST = "10.253.9.151"  # Escuchar en una IP específica
PORT = 5001  # Puerto de escucha
MODEL_PATH = "clap_network.h5"  # Modelo entrenado
SAMPLE_RATE = 44100

# Cargar modelo de IA
model = tf.keras.models.load_model(MODEL_PATH)

# Iniciar servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"🔍 Servidor escuchando en {HOST}:{PORT}...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"📥 Conexión establecida con {client_address}")
    
    # Recibir datos de audio
    audio_data = b""
    while True:
        packet = client_socket.recv(4096)
        if not packet:
            break
        audio_data += packet
    
    print("✅ Audio recibido.")
    print(f"📦 Datos recibidos (bytes): {audio_data}")
    print(f"📏 Tamaño de los datos recibidos: {len(audio_data)}")
    
    # Asegurar que los datos recibidos tienen un tamaño válido
    if len(audio_data) % 2 != 0:
        print("⚠️ Advertencia: Tamaño incorrecto del buffer, descartando datos.")
        continue  # Saltar esta iteración si los datos son inválidos

    # Convertir los bytes en un array de enteros
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    print(f"📊 Datos convertidos: {audio_array}")

    # Verificar si el audio solo contiene ceros
    max_value = np.max(np.abs(audio_array))
    if max_value == 0:
        print("⚠️ Error: El audio recibido solo contiene ceros, descartando datos.")
        continue  # Saltar a la próxima iteración del loop

    # Normalizar el audio
    audio_array = audio_array.astype(np.float32) / max_value
    print(f"📉 Datos normalizados: {audio_array}")

    # Convertir en espectrograma
    S = librosa.feature.melspectrogram(y=audio_array, sr=SAMPLE_RATE)
    S_db = librosa.power_to_db(S, ref=np.max)

    # Preparar el espectrograma para la IA
    S_db = np.expand_dims(S_db, axis=[0, -1])  # Agregar dimensiones necesarias
    prediction = model.predict(S_db)[0][0] * 100

    # Determinar si fue un aplauso
    response = "1" if prediction > 90 else "0"
    client_socket.send(response.encode())
    print(f"📤 Respuesta enviada: {response}")

    client_socket.close()
