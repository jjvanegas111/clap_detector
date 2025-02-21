import socket
import numpy as np
import librosa
import tensorflow as tf
from scipy.io.wavfile import write

# Configuración del servidor
HOST = "0.0.0.0"  # Escuchar en todas las interfaces de red
PORT = 5000  # Puerto de escucha
MODEL_PATH = "clap_network.h5"  # Modelo entrenado
AUDIO_PATH = "received_audio.wav"
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
    
    # Guardar el audio recibido
    with open(AUDIO_PATH, "wb") as f:
        f.write(audio_data)
    
    print("✅ Audio recibido y guardado.")
    
    # Cargar el audio para la IA
    y, sr = librosa.load(AUDIO_PATH, sr=SAMPLE_RATE)
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_db = librosa.power_to_db(S, ref=np.max)
    
    # Preparar el espectrograma para la IA
    S_db = np.expand_dims(S_db, axis=[0, -1])  # Agregar dimensiones necesarias
    prediction = model.predict(S_db)[0][0] * 100
    
    # Determinar si fue un aplauso
    response = "1" if prediction > 90 else "0"
    client_socket.send(response.encode())
    print(f"📤 Respuesta enviada: {response}")
    
    client_socket.close()
