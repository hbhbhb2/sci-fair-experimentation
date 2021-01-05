# what the ai guesses the characters read out

from PIL import Image, ImageDraw
import pytesseract
import sys
import os
from pathlib import Path
from separator import separate_img
import tensorflow as tf
import numpy as np

# path to AI's saved weights
CP_PATH = Path('./saves')

# gets names of each label in AI
CLASSNAMES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ-'"

# this fn creates a clean TF model, which can be loaded with a past save state to get an AI
def create_model() -> tf.keras.Model:
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

def create_prob_model(model: tf.keras.Model) -> tf.keras.Model:
    return tf.keras.Sequential([model, tf.keras.layers.Softmax()])

zero_model = create_model()
zero_prob_model = create_prob_model(zero_model)

zero_model.save_weights('saves/zero/checkpoint')
# create the model & convert it into probabilities
model = create_model()
latest = tf.train.latest_checkpoint(CP_PATH)
model.load_weights(latest)
prob_model = create_prob_model(model)

past_state = None

# only reload weights if the state changes. prevents the model being reloaded 80x in benchmark
def get_model(period: int) -> tf.keras.Model:
    global past_state
    if period == None: return prob_model
    if period == past_state: return prob_model
    past_state = period

    # state before training
    if period == 0: return zero_prob_model

    # get ckpt matching period
    epoch = period * 15
    state_path = os.path.join(CP_PATH, f"cp-{epoch:04d}.ckpt")
    model.load_weights(state_path)
    return create_prob_model(model)

# main guessing fn. 
# This function takes an image with handwriting, optionally a model and a specific checkpoint #
# The function takes the image, separates it out, and reads out the model's guess
def guess(img: Image.Image, *, state: int = None) -> str:
    # set the model of the current state
    model = get_model(state)

    # separate the image into a list of images (each being a character), then convert each character into its numpy array equivalent (which can then be plugged into the TF model)
    chrs = separate_img(img)
    chrs_np = [tf.keras.preprocessing.image.img_to_array(char)[None, :, :] for char in chrs]

    # for each character, plug in each guess through the model, pick the guess it is MOST confident about.
    buf = ""
    for char in chrs_np:
        i = np.argmax(model(char))
        buf += CLASSNAMES[i]

    return buf


# if script is ran as a SCRIPT (i.e. "python3 scripts/ai_guess.py [args]" in the command line), run the guess image on arguments.
if __name__ == '__main__':
    input_img = Image.open(sys.argv[1])
    print(guess(input_img))
    print(guess(input_img, state=0))
    print(guess(input_img, state=1))
    print(guess(input_img, state=2))
    print(guess(input_img, state=3))
    print(guess(input_img, state=4))
    print(guess(input_img, state=5))
    print(guess(input_img, state=6))
    print(guess(input_img, state=7))
    print(guess(input_img, state=8))
    