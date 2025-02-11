import sounddevice as sd
import numpy as np
import tensorflow as tf
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import time
from scipy.io.wavfile import write

# Cargar el modelo entrenado
model = tf.keras.models.load_model("clap_detection_model.h5")

# Configuración de audio
sample_rate = 44100  # Frecuencia de muestreo
chunk_duration = 2  # Duración de cada grabación en segundos
chunk_samples = int(chunk_duration * sample_rate)  # Cantidad de muestras por chunk
output_dir = "live_spectrograms"  # Carpeta para guardar los espectrogramas

# Crear la carpeta si no existe
os.makedirs(output_dir, exist_ok=True)

# Contador para nombrar los archivos
counter = 0

def capture_audio():
    """ Captura audio del micrófono y lo devuelve como un array numpy """
    print("🎤 Escuchando...")
    recording = sd.rec(chunk_samples, samplerate=sample_rate, channels=1, dtype=np.float32)
    sd.wait()
    return np.squeeze(recording)

def generate_spectrogram(audio, filename):
    """ Genera un espectrograma a partir de un audio y lo guarda como imagen """
    plt.figure(figsize=(1.28, 1.28))  # 128x128 píxeles
    S = librosa.feature.melspectrogram(y=audio, sr=sample_rate, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    librosa.display.specshow(S_dB, sr=sample_rate, cmap='inferno')
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"📷 Espectrograma guardado: {filename}")

def predict_clap():
    """ Captura audio, genera su espectrograma, lo guarda y usa para predecir un aplauso """
    global counter
    audio = capture_audio()
    
    # Guardar espectrograma en la carpeta "live_spectrograms"
    spec_filename = os.path.join(output_dir, f"spectrogram_{counter}.png")
    generate_spectrogram(audio, spec_filename)
    counter += 1  # Incrementar el contador para el próximo archivo

    # Cargar la imagen del espectrograma
    img = tf.keras.preprocessing.image.load_img(spec_filename, target_size=(128, 128))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Hacer la predicción
    prediction = model.predict(img_array)[0][0]
    
    if prediction > 0.9:
        print("👏 Aplauso detectado!")
    else:
        print(".", end="", flush=True)

# Loop en vivo
print("Iniciando detección de aplausos...")
while True:
    predict_clap()
    time.sleep(2)  # Espera 2 segundos antes de la próxima captura