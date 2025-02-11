import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

# Directorios de los audios
applause_dir = "noise2"
#noise_dir = "dataset_expandido/ruidos"
spectrogram_applause_dir = "dataset_spectrograms1/"
#spectrogram_applause_dir = "dataset_spectrograms/aplausos"
#spectrogram_noise_dir = "dataset_spectrograms/ruidos"

# Crear directorios de salida
os.makedirs(spectrogram_applause_dir, exist_ok=True)
#os.makedirs(spectrogram_noise_dir, exist_ok=True)

def generate_spectrogram(input_path, output_path):
    """Genera y guarda el espectrograma de un archivo de audio con tamaño 128x128 píxeles."""
    y, sr = librosa.load(input_path, sr=None)
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_DB = librosa.power_to_db(S, ref=np.max)
    
    plt.figure(figsize=(1.28, 1.28), dpi=100)  # 1.28 x 100 = 128 píxeles
    plt.axis('off')
    librosa.display.specshow(S_DB, sr=sr, cmap='viridis')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def convert_audios_to_spectrograms(input_dir, output_dir):
    """Convierte todos los audios en una carpeta a espectrogramas."""
    files = [f for f in os.listdir(input_dir) if f.endswith(".wav")]
    for file in files:
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file.replace(".wav", ".png"))
        generate_spectrogram(input_path, output_path)
    print(f"Se generaron espectrogramas en {output_dir}")

# Generar espectrogramas
convert_audios_to_spectrograms(applause_dir, spectrogram_applause_dir)
#convert_audios_to_spectrograms(noise_dir, spectrogram_noise_dir)


