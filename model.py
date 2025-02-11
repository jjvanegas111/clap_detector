import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Directorios de los espectrogramas
spectrogram_dir = "dataset_spectrograms"
batch_size = 32
img_size = (128, 128)

# Generadores de datos para entrenamiento y validación
datagen = ImageDataGenerator(validation_split=0.2, rescale=1./255)
train_generator = datagen.flow_from_directory(
    spectrogram_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='binary',
    subset='training'  # 80% de los datos para entrenamiento
)
val_generator = datagen.flow_from_directory(
    spectrogram_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='binary',
    subset='validation' # 20% de los datos para validación
)

# Definición del modelo
model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

# Compilación del modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entrenamiento del modelo
epochs = 5
model.fit(train_generator, epochs=epochs, validation_data=val_generator)

# Guardar el modelo entrenado
model.save("clap_network.h5")
