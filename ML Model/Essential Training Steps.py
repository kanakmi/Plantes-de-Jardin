# import the required libraries

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import tensorflow as tf
from tensorflow.keras import layers, optimizers
from tensorflow.keras.layers import *
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Global Variable for later use

IMAGE_SIZE = 128
BATCH_SIZE = 32
CHANNELS = 3

# There are 24826 Images in our Dataset belonging to different diseases associated with 
# Corn, Pepper Bell, Potato and Tomato

dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "PlantVillage",
    seed=123, # this will ensure we get the same images each time
    shuffle=True, # images inside the batches will be shuffled
    image_size=(IMAGE_SIZE,IMAGE_SIZE), # every image will be of 256x256 dimention
    batch_size=BATCH_SIZE # There will be 32 images in each batch
)

# The Images belong to the following Class Labels
'''
Class names are as follows-
['Corn Blight',
 'Corn Common_Rust',
 'Corn Gray_Leaf_Spot',
 'Corn Healthy',
 'Pepper_Bell Bacterial_Spot',
 'Pepper_Bell Healthy',
 'Potato Early_Blight',
 'Potato Healthy',
 'Potato Late_Blight',
 'Tomato Bacterial_Spot',
 'Tomato Early_Blight',
 'Tomato Healthy',
 'Tomato Late_Blight',
 'Tomato Leaf_Mold',
 'Tomato Mosaic_Virus',
 'Tomato Septoria_Leaf_Spot',
 'Tomato Spider_Mites',
 'Tomato Target_Spot',
 'Tomato YellowLeaf__Curl_Virus']
'''
class_names = dataset.class_names

'''
Splitting the dataset
We will take -
- 80% data for training our model
- 10% data for validation purpose
- 10% data for test purpose
'''

# total batches of data = 776

train_ds = dataset.take(620) # 80% of 776
test_ds = dataset.skip(620) # remaining 20%
val_ds = test_ds.take(78) # 10% of 776
test_ds = test_ds.skip(78) # 10% of 776

# Cache, Shuffle and Prefetch the dataset to train the model faster

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)
val_ds = val_ds.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)
test_ds = test_ds.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)

# Data Augmentation Layer 
# Augmentation is the process of creating new training samples by altering the available data.

data_augmentation = tf.keras.Sequential([
    layers.experimental.preprocessing.RandomFlip("horizontal_and_vertical"),
    layers.experimental.preprocessing.RandomRotation(0.2),
])

# Applying Augmentation on Training Data
train_ds = train_ds.map(
    lambda x, y: (data_augmentation(x, training=True), y)
).prefetch(buffer_size=tf.data.AUTOTUNE)

# Designing and Training the Model

# Reshaping so that each image is of same size and rescaling images them for normalization
resize_and_rescale = tf.keras.Sequential([
    layers.experimental.preprocessing.Resizing(IMAGE_SIZE, IMAGE_SIZE),
    layers.experimental.preprocessing.Rescaling(1./255),
])

input_shape = (BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNELS)
n_classes = 19

# creating a sequential model
model = tf.keras.Sequential([
    resize_and_rescale,
    Conv2D(filters=32, kernel_size=(2,2), activation='relu', input_shape=input_shape),
    MaxPooling2D((4,4)),
    
    Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'),
    MaxPooling2D((3,3)),
    Dropout(0.3), # for regularization
    
    Conv2D(filters=64, kernel_size=(4,4), activation='relu', padding='same'),
    Conv2D(filters=128, kernel_size=(5,5), activation='relu', padding='same'),
    MaxPooling2D((2,2)),
    Dropout(0.4),
    
    Conv2D(filters=128, kernel_size=(5,5), activation='relu', padding='same'),
    MaxPooling2D((2,2)),
    Dropout(0.5),
    
    Flatten(), # flattening for feeding into ANN
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dense(n_classes, activation='softmax')
])

model.build(input_shape=input_shape)

# Slowing down the learning rate
opt = optimizers.Adam(learning_rate=0.0001)

# compile the model
model.compile(loss = 'sparse_categorical_crossentropy', optimizer=opt, metrics= ["accuracy"])

# use early stopping to exit training if validation loss is not decreasing even after certain epochs (patience)
earlystopping = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=20)

# save the best model with least validation loss
checkpointer = ModelCheckpoint(filepath="plantvillage_weights.h5", verbose=1, save_best_only=True)

history = model.fit(train_ds, epochs = 100, validation_data=val_ds, batch_size=BATCH_SIZE, shuffle=True, callbacks=[earlystopping, checkpointer])

# save the model architecture to json file for future use

model_json = model.to_json()
with open("plantvillage_model.json","w") as json_file:
    json_file.write(model_json)

# Load pretrained model (best saved one)
with open('plantvillage_model.json', 'r') as json_file:
    json_savedModel= json_file.read()
# load the model  
model = tf.keras.models.model_from_json(json_savedModel)
model.load_weights('plantvillage_weights.h5')
model.compile(loss = 'sparse_categorical_crossentropy', optimizer=opt, metrics= ["accuracy"])

scores = model.evaluate(test_ds)

print(scores)