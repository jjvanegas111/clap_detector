import os
import shutil
import librosa
import numpy as np
import soundfile as sf
import random

# Directorios de los audios
applause_dir = "dataset/aplausos"
noise_dir = "dataset/ruidos"
output_applause_dir = "dataset_expandido/aplausos"
output_noise_dir = "dataset_expandido/ruidos"

# Crear directorios de salida
os.makedirs(output_applause_dir, exist_ok=True)
os.makedirs(output_noise_dir, exist_ok=True)

def modify_audio(input_path, output_path):
    """Aplica pequeñas modificaciones al audio para evitar duplicados exactos."""
    y, sr = librosa.load(input_path, sr=None)
    
    # Modificaciones aleatorias
    if random.choice([True, False]):
        y = librosa.effects.time_stretch(y, rate=random.uniform(0.9, 1.1))  # Cambio de velocidad
    if random.choice([True, False]):
        y = y + np.random.normal(0, 0.005, y.shape)  # Ruido aleatorio
    
    sf.write(output_path, y, sr)

# Función para duplicar y modificar audios
def duplicate_audios(input_dir, output_dir, target_count):
    files = [f for f in os.listdir(input_dir) if f.endswith(".wav")]
    current_count = len(files)
    
    if current_count == 0:
        print(f"No hay archivos en {input_dir}")
        return
    
    index = 0
    while current_count < target_count:
        file_to_copy = files[index % len(files)]
        new_file_name = f"{current_count}.wav"
        output_path = os.path.join(output_dir, new_file_name)
        
        modify_audio(os.path.join(input_dir, file_to_copy), output_path)
        current_count += 1
        index += 1
    
    print(f"Se generaron {current_count} archivos en {output_dir}")

# Ejecutar duplicación
duplicate_audios(applause_dir, output_applause_dir, 999)
duplicate_audios(noise_dir, output_noise_dir, 999)
