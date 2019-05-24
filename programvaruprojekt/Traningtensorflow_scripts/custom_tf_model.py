import os
import pickle
import time
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
"""[summary]
This file handels the traning of a custom tf model
The code is based on sentdex youtube tutorial see link below
https://www.youtube.com/watch?v=WvoLTXIjBYU&list=PLQVvvaa0QuDfhTox0AjmQ6tvTgMBZBEXN&index=3
Author:Daniel Persson 2019-05-21
"""
#Variables to change
EPOCHS = 10
BATCH_SIZE = 100
VALIDATION_SPLIT = 0.3

#The array names
XARRAY = "NAME_OF_ARRAY_X.pickle"
YARRAY = "NAME_OF_ARRAY_Y.pickle"

dense_layers = [0]
layer_sizes = [256]
conv_layers = [2]

#Create paths to array
LOCATION_PATH = Path.cwd().parent / "tensorflowdata"
#Location to input data
DATAIN = LOCATION_PATH / "tensorflowarrays"

#Create folders
def create_folders():
    try:
        os.makedirs(LOCATION_PATH / "tensorflowmodels")
    except:
        pass
    try:
        os.makedirs(LOCATION_PATH / "tensorflowlogs")
    except:
        pass

create_folders()

XARRAY_PATH = DATAIN / XARRAY
YARRAY_PATH = DATAIN / YARRAY

#Get arrays
pickle_in = open(XARRAY_PATH,"rb")
X = pickle.load(pickle_in)

pickle_in = open(YARRAY_PATH,"rb")
Y = pickle.load(pickle_in)

X = X/255.0

for dense_layer in dense_layers:
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            name = "{}-conv-{}-nodes-{}-dense-{}".format(conv_layer,layer_size,dense_layer,int(time.time()))
            tensorboard = TensorBoard(log_dir=LOCATION_PATH / "tensorflowlogs" / name)
            #Modelname
            modelname = name+".model"
            #Create path for model
            model_path = LOCATION_PATH / "tensorflowmodels" / modelname
            #Layers - Change if needed
            model = Sequential()

            model.add(Conv2D(layer_size, (3, 3), input_shape=X.shape[1:]))
            model.add(Activation('relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))

            for l in range(conv_layer-1):
                model.add(Conv2D(layer_size, (3, 3)))
                model.add(Activation('relu'))
                model.add(MaxPooling2D(pool_size=(2, 2)))

            model.add(Flatten())
            for l in range(dense_layer):
                model.add(Dense(layer_size))
                model.add(Activation('relu'))

            model.add(Dense(1))
            model.add(Activation('sigmoid'))

            model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

            model.fit(X, Y, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=VALIDATION_SPLIT,callbacks=[tensorboard])
            model.save(model_path)