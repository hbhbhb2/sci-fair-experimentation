# what the ai guesses the characters read out

from PIL import Image, ImageDraw
import pytesseract
import sys
from pathlib import Path
from separator import separate_img
import tensorflow as tf
import numpy as np

input_path = Path(sys.argv[1])
AI_PATH = Path('./ai/checkers')

img = Image.open(input_path)
chr_list = separate_img(img)
chr_arr = [tf.keras.preprocessing.image.img_to_array(char)[None, :, :] for char in chr_list]
classnames = "ABCDEFGHIJKLMNOPQRSTUVWXYZ-'"

def create_model():
    model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(32, 32, 1)),
    tf.keras.layers.Dense(128,activation='relu'),
    tf.keras.layers.Dense(28)
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    return model

model = create_model()
model.load_weights(AI_PATH)
prob_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

for chr_img in chr_arr:
    i = np.argmax(prob_model(chr_img))
    print(classnames[i])