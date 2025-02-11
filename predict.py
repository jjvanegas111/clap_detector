import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Configuración
model_path = "clap_network.h5"  # Modelo entrenado
dataset_path = "live_spectrograms"  # Carpeta con los espectrogramas

# Cargar el modelo
model = tf.keras.models.load_model(model_path)
print("✅ Modelo cargado correctamente.")

# Obtener la lista de imágenes en la carpeta
image_files = [f for f in os.listdir(dataset_path) if f.endswith(".png")]
if not image_files:
    print("⚠️ No se encontraron imágenes en la carpeta 'live_spectrograms'.")
    exit()

# Cargar imágenes y hacer predicciones
correct = 0
total = len(image_files)

print(f"🔍 Analizando {total} espectrogramas...\n")

for img_name in image_files:
    img_path = os.path.join(dataset_path, img_name)
    
    # Cargar la imagen y preprocesarla
    img = load_img(img_path, target_size=(128, 128))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Hacer la predicción
    prediction = model.predict(img_array)[0][0] * 100
    
    if prediction > 0.9:
        print(f"{img_name}: 👏 ({prediction:.1f}%)")
        correct += 1
    else:
        print(f"{img_name}: ❌ ({prediction:.1f}%)")


