# -*- coding: utf-8 -*-
"""Ahmad Nicolas Raffael DicodingIndosat1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1J5ENv18n_m90xLiK006PPrCD8VhBWzds
"""

import zipfile
import os
import urllib.request

url = 'https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip'
filename = 'rockpaperscissors.zip'
urllib.request.urlretrieve(url, filename)

with zipfile.ZipFile(filename, 'r') as archive:
    archive.extractall()

print(os.listdir('rockpaperscissors'))

from tensorflow.keras.preprocessing.image import ImageDataGenerator

data_directory = 'rockpaperscissors/rps-cv-images'

data_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    horizontal_flip=True,
    shear_range=0.15,
    zoom_range=0.1,
    fill_mode='nearest',
    validation_split=0.4
)

training_data = data_gen.flow_from_directory(
    data_directory,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

validation_data = data_gen.flow_from_directory(
    data_directory,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

import tensorflow as tf
from tensorflow.keras import layers, models

nn_model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(3, activation='softmax')
])

nn_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                 loss='categorical_crossentropy',
                 metrics=['accuracy'])

steps_per_epoch = 1314 // 32
validation_steps = 874 // 32

history = nn_model.fit(
    training_data,
    steps_per_epoch=steps_per_epoch,
    epochs=20,
    validation_data=validation_data,
    validation_steps=validation_steps,
    verbose=2
)

from google.colab import files
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

uploaded_images = files.upload()

labels = ['rock', 'paper', 'scissors']

for img_file in uploaded_images.keys():
    img = image.load_img(img_file, target_size=(150, 150))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = nn_model.predict(img_array)
    predicted_label = labels[np.argmax(prediction)]

    plt.imshow(image.load_img(img_file))
    plt.title(f'Prediction: {predicted_label}')
    plt.axis('off')
    plt.show()

import matplotlib.pyplot as plt

training_accuracy = history.history['accuracy']
validation_accuracy = history.history['val_accuracy']
training_loss = history.history['loss']
validation_loss = history.history['val_loss']

epochs = range(len(training_accuracy))

plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.plot(epochs, training_accuracy, label='Training Accuracy')
plt.plot(epochs, validation_accuracy, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs, training_loss, label='Training Loss')
plt.plot(epochs, validation_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()