# -*- coding: utf-8 -*-
"""CNN.ipynb

Automatically generated by Colaboratory.
Convolutional Neural Network in python using Google Colab

"""

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.callbacks import EarlyStopping
import keras
from time import time

K.clear_session()


# ----- Tratamiento de las imágenes (dataset) -----

train_data_dir = '/content/drive/My Drive/Colab/Datasets/Train/'
validation_data_dir = '/content/drive/My Drive/Colab/Datasets/Validation/'

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.3,
        zoom_range=0.3,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(150, 150),
        batch_size=15,
        class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(150, 150),
        batch_size=5,
        class_mode='categorical')

# ----- Creación del modelo ----- 

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(150, 150, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))

model.add(Dropout(0.5))
model.add(Dense(4, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

#  ----- Entrenamiento ----- 

epochs = 20

es = EarlyStopping(monitor='val_accuracy', mode='max', verbose=1, patience=3, restore_best_weights=True)

history = model.fit_generator(
        train_generator,
        steps_per_epoch=100,
        epochs=epochs, 
        validation_data=validation_generator,
        validation_steps12850,
)

#  ----- Guardamos el modelo  ----- 

model.save("/content/drive/My Drive/Colab/mimodelo.h5")

#  ----- Gráfica accuracy ----- 

from matplotlib import pyplot as plt

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='validation accuracy')

plt.title('Accuracy entreno RN FSI')
plt.xlabel('Épocas')
plt.legend(loc="lower right")

plt.show()

#  ----- Gráfica loss ----- 

from matplotlib import pyplot as plt

plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='validation loss')

plt.title('Loss entreno RN FSI')
plt.xlabel('Épocas')
plt.legend(loc="lower right")

plt.show()

#  ----- Predicción de una imagen ----- 

from matplotlib.pyplot import imshow
import numpy as np
from PIL import Image
import keras

model = keras.models.load_model("/content/drive/My Drive/Colab/mimodelo.h5")

# %matplotlib inline
pil_im = Image.open("/content/drive/My Drive/Colab/Datasets/Predict/car/car1.jpg")
im = np.asarray(pil_im.resize((150, 150)))
imshow(im)

im = im.reshape(1,150,150,3)
guess = model.predict(im)
res = guess[0]
print(res)

if np.argmax(res) == 0:
  print("Coche")
elif np.argmax(res) == 1:
  print("Gorila")
elif np.argmax(res) == 2:
  print("Panda")
else:
  print("Perro")
