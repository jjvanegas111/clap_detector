import os
import time
import numpy as np
import sounddevice as sd
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# Configuración
DURATION = 2  # Duración de cada grabación en segundos
SAMPLE_RATE = 44100  # Frecuencia de muestreo
OUTPUT_DIR = "live_spectrograms"  # Carpeta donde se guardarán los espectrogramas

# Crear la carpeta si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

def record_audio(filename):
    """Graba 2 segundos de audio y lo guarda en un archivo WAV"""
    print("🎤 Grabando...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
    sd.wait()  # Esperar a que termine la grabación
    write(filename, SAMPLE_RATE, audio)
    print(f"✅ Audio guardado: {filename}")

def generate_spectrogram(audio_path, output_path):
    """Genera y guarda el espectrograma de un archivo de audio"""
    y, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_db = librosa.power_to_db(S, ref=np.max)

    plt.figure(figsize=(2, 2))  # 128x128 px
    librosa.display.specshow(S_db, sr=sr, cmap='inferno')
    plt.axis('off')  # Ocultar ejes
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=64)  # Guardar espectrograma
    plt.close()
    print(f"📷 Espectrograma guardado: {output_path}")

# Bucle infinito para capturar audio y generar espectrogramas cada 2 segundos
counter = 0
while True:
    audio_filename = f"temp_audio.wav"
    spectrogram_filename = os.path.join(OUTPUT_DIR, f"spectrogram_{counter}.png")

    # Grabar audio y generar espectrograma
    record_audio(audio_filename)
    generate_spectrogram(audio_filename, spectrogram_filename)

    counter += 1
    time.sleep(2)  # Esperar antes de la siguiente captura