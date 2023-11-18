# -*- coding: utf-8 -*-
"""Drowsiness detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/187tJbEMCwcTmSm3tMFLMMF33sNFYmm1U

# Drowsiness Detection


In todays world 21% of accidents are happening due to drowsy driving. sleep related crashes are most common in young people between the ages of 18 and 29. There can be many causes like lack of sleep, tiredness, driving long distance alone may lead to feel drowsiness while driving car.
In this project we will build a Neural network model which will be able to predict if person is drowsy or not.
Drowsiness detection can be used in cars to detect if driver is feeling drowsy while driving car, this will alert the driver and will help to avoid many car accidents.

Let's first import the libraries required to build model
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""# **Image preprocessing and Augmentation**

Image preprocessing is used to clean data before used by computer vision model. This makes sure all the image size array are of same size, if your image array size is not equal then computer vision model won't be able to work properly.

Image augmentation is used to improve training dataset by creating different versions of similar contents so that model can have exposure to wide array of training set.
Image augmentation is applied to training dataset only.


Keras ImageDataGenerator helps for Image pre-processing, Augmentation and splitting dataset into train and test datasets.
"""

from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(rescale=1./255, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.5)

train_generator = train_datagen.flow_from_directory(
        '/content/drive/MyDrive/ImprovementSet',
        target_size=(254, 254),
        batch_size=5755,
        class_mode='binary',
        shuffle=True,
        subset='training',
        seed=42)

test_generator = test_datagen.flow_from_directory(
        '/content/drive/MyDrive/TestSet',
        target_size=(254, 254),
        batch_size=2116,
        class_mode='binary',
        subset="training",
        shuffle=True,
        seed=42)


valid_generator = test_datagen.flow_from_directory(
        '/content/drive/MyDrive/TestSet',
        target_size=(254, 254),
        batch_size=2116,
        class_mode='binary',
        subset="validation",
        shuffle=True,
        seed=42)

"""Keras image data generator has extracted the images to directory form. To feed the images to model for training we need to export it as array.

**Exporting Training dataset**
"""

X, Y = next(train_generator)

x_train = np.array(X)
y_train = np.array(Y)

x_train.shape

"""**Exporting test dataset**"""

X, Y = next(test_generator)

x_test = np.array(X)
y_test = np.array(Y)

x_test.shape

"""**Exporting valid dataset**"""

X, Y = next(valid_generator)

x_valid = np.array(X)
y_valid = np.array(Y)

"""Let's print the images from training dataset."""

plt.imshow(x_train[0])

print(y_train[0])

plt.imshow(x_train[500])

print(y_train[500])

Eyes = ["Closed", "Opened"]

plt.figure(figsize=(15,8))
plt.subplot(2,3,1)
img = x_train[250]
plt.imshow(img)
print(y_train[250])
f = Eyes[(y_train[250]).astype(int)]
plt.title(f)
plt.axis("off")

print(x_train.shape)

"""**Let's build CNN model**"""

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import layers, models

model_eye = models.Sequential([
    layers.Conv2D(filters=254, kernel_size=(3,3), activation='relu',input_shape=(254, 254, 3)),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(filters=150, kernel_size=(3,3), activation='relu',input_shape=(254, 254, 3)),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(filters=500, kernel_size=(3,3), activation='relu',input_shape=(254, 254, 3)),
    layers.MaxPooling2D((2,2)),
    layers.Flatten(),

  Dense(units = 100, activation ='relu'),
  Dense(units = 150, activation = 'relu'),
  Dense(units = 1, activation = 'sigmoid')

])

model_eye.compile(optimizer="adam", loss='binary_crossentropy',
              metrics=['accuracy'])

from keras.callbacks import EarlyStopping

early_stopping = EarlyStopping(monitor='val_loss', patience=3)
valid_set=(x_valid, y_valid)

model_eye.fit(x_train, y_train, validation_data = valid_set, epochs=20, callbacks=[early_stopping])

train_acc = model_eye.evaluate(x_train, y_train)
print("Train data accuracy= ", train_acc)

y_train_pred = model_eye.predict(x_train)
print(y_train_pred[1])
y_p = [np.argmax(i) for i in y_train_pred]

p_pred = y_train_pred.flatten()
print(p_pred.round(0))

from sklearn import metrics

# p_pred = model.predict(X_test)
y_train_pred = p_pred.round(0)
# [1. 0.01 0.91 0.87 0.06 0.95 0.24 0.58 0.78 ...

# extract the predicted class labels
y_pred = np.where(p_pred > 0.5, 1, 0)
print(y_pred)

confusion_matrix = metrics.confusion_matrix(y_train, y_train_pred)

cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = ["Closed", "Opened"])

cm_display.plot()
plt.show()

y_test_p = model_eye.predict(x_test)
print(y_pred[1])
y_p = [np.argmax(i) for i in y_pred]

p_test_p = y_test_p.flatten()
print(p_pred.round(0))
y_test_p = p_test_p.round(0)



test_acc = model_eye.evaluate(x_test, y_test)
print("Test data accuracy= ", test_acc)

from sklearn import metrics



confusion_matrix_test = metrics.confusion_matrix(y_test, y_test_p)

cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix_test, display_labels = ["Closed", "Opened"])

cm_display.plot()
plt.show()

# showing image
plt.imshow(x_test[950])

plt.title(Eyes[int(y_test_p[950])])

plt.imshow(x_test[35])

plt.title(Eyes[int(y_test_p[35])])