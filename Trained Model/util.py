import numpy as np
import tensorflow as tf
from PIL import Image

with open('plantvillage_model.json', 'r') as json_file:
    json_savedModel = json_file.read()

# load the model architecture
model = tf.keras.models.model_from_json(json_savedModel)
model.load_weights('plantvillage_weights.h5')
opt = tf.keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=opt,loss="sparse_categorical_crossentropy", metrics=["accuracy"])

labels = ['Corn Blight',
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


def classify_image(file_path):
    image = Image.open(file_path) # reading the image
    img = np.asarray(image) # converting it to numpy array
    img = np.expand_dims(img, 0)
    predictions = model.predict(img) # predicting the class
    c = np.argmax(predictions[0]) # extracting the class with maximum probablity
    cls = (labels[c]).split()
    probab = float(round(predictions[0][c]*100, 2))

    result = {
        'plant': cls[0],
        'status': cls[1],
        'probablity': probab
    }

    return result
