# Science Fair Dataset Making & Testing Scripts

## Scripts

* python3 [ai_guess.py](scripts/ai_guess.py) [args]
  * Provides the AI's guess on what is being displayed.
  * An input image is separated into individual characters, input through the AI system, and the result is returned.
* python3 [bounding_box_gen.py](scripts/bounding_box_gen.py) [args]
  * Draws bounding boxes around the image at the specified path provided using pytesseract.
* python3 [control.py](scripts/control.py) [args]
  * Gives pytesseract's guess on what the image at the specified path reads.
* python3 [create_train_data.py](scripts/create_train_data.py)
  * Creates training data by separating images by bounding boxes and filtering out hard-to-manage outputs.
  * The generated dataset can be found in the Google Colab, and the code for converting the dataset into a TensorFlow dataset is here (https://github.com/hbhbhb2/sci_fair_dataset).
* python3 [separator.py](scripts/separator.py)
  * This script contains a function (separate_img) simply takes an image, separates it into a list of character images via pytesseract.
