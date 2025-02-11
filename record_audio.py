import sounddevice as sd
import numpy as np
import wave
import os

# Configuración de grabación
SAMPLE_RATE = 44100  # Frecuencia de muestreo
DURATION = 2  # Duración de la grabación en segundos
DATASET_PATH = "dataset_5"  # Carpeta donde se guardarán los archivos

# Crear carpeta si no existe
os.makedirs(DATASET_PATH, exist_ok=True)

def record_audio(label, sample_num):
    print(f"Grabando {label} {sample_num}...")
    audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
    sd.wait()
    
    # Guardar el archivo
    filename = f"{DATASET_PATH}/{label}_{sample_num}.wav"
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16 bits
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())
    
    print(f"Guardado: {filename}")

# Grabación de muestras
num_samples = 10  # Número de muestras por categoría
for i in range(num_samples):
    input("Presiona Enter para grabar un aplauso...")
    record_audio("aplauso", i)
    input("Presiona Enter para grabar ruido...")
    record_audio("ruido", i)

print("Grabación completada.")
