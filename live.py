import os
import time
import numpy as np
import sounddevice as sd
import librosa
import librosa.display
import matplotlib.pyplot as plt
import tensorflow as tf
from scipy.io.wavfile import write
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Configuración
DURATION = 2  # Duración de cada grabación en segundos
SAMPLE_RATE = 44100  # Frecuencia de muestreo
OUTPUT_DIR = "live_spectrograms_verdes"  # Carpeta donde se guardarán los espectrogramas
MODEL_PATH = "clap_network.h5"  # Ruta del modelo entrenado

# Crear la carpeta si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cargar modelo entrenado
model = tf.keras.models.load_model(MODEL_PATH)
#print("✅ Modelo cargado correctamente.")

# Listar dispositivos de audio disponibles
def list_audio_devices():
    print("\n🎤 Dispositivos de audio disponibles: ")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"[{i}] {device['name']} - Input Channels: {device['max_input_channels']}")

# Permitir al usuario elegir un dispositivo de entrada
list_audio_devices()
device_index = int(input("\nIngresa el número del dispositivo que deseas usar: "))

def record_audio(filename):
    """Graba 2 segundos de audio y lo guarda en un archivo WAV"""
    print(".")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16, device=device_index)
    sd.wait()
    write(filename, SAMPLE_RATE, audio)
    #print(f"✅ Audio guardado: {filename}")

def generate_spectrogram(audio_path, output_path):
    """Genera y guarda el espectrograma de un archivo de audio"""
    y, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_db = librosa.power_to_db(S, ref=np.max)

    plt.figure(figsize=(2, 2))  # 128x128 px
    librosa.display.specshow(S_db, sr=sr, cmap='viridis')
    plt.axis('off')  # Ocultar ejes
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=64)
    plt.close()
    #print(f"📷 Espectrograma guardado: {output_path}")

def predict_clap(spectrogram_path):
    """Carga el espectrograma y hace la predicción."""
    img = load_img(spectrogram_path, target_size=(128, 128))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array, verbose=0)[0][0] * 100
    return prediction

# Bucle infinito para capturar y analizar audio en vivo
print("\n🔍 Escuchando en tiempo real... Presiona Ctrl + C para detener")
counter = 0

try:
    while True:
        audio_filename = "temp_audio.wav"
        spectrogram_filename = os.path.join(OUTPUT_DIR, f"spectrogram_{counter}.png")

        # Grabar audio y generar espectrograma
        record_audio(audio_filename)
        generate_spectrogram(audio_filename, spectrogram_filename)

        # Hacer la predicción
        prediction = predict_clap(spectrogram_filename)
        if prediction > 50:
            print(f"👏 ({prediction:.1f}%) #{counter}")
        #else:
            #print(f".")

        counter += 1
        time.sleep(0.5)  # Esperar antes de la siguiente captura
except KeyboardInterrupt:
    print("🛑 Detección detenida por el usuario.")

