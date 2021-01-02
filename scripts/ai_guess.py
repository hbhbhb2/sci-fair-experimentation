# what the ai guesses the characters read out

# TODO (once the AI is complete)

from PIL import Image
import pytesseract
import sys
from pathlib import Path
from separator import separate_img

input_path = Path(sys.argv[0])
chr_list = separate_img(Image.open(input_path))

for chr_img in chr_list:
    # TODO AI STUFF!!
    pass