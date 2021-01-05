# control: what pytesseract (the OCR software) perceives the image says

from PIL import Image
import pytesseract
import sys

# use pytesseract's guess on what the image reads
def control(img: Image.Image) -> str:
    guess = pytesseract.image_to_string(img)

    # normalize the guess to look like our AI's guess
    return guess.strip().upper()


# if script is ran as a SCRIPT (i.e. "python3 scripts/control.py [args]" in the command line), run the control guess on arguments.
if __name__ == '__main__':
    input_img = Image.open(sys.argv[1])
    guess = control(input_img)
    print(guess)
    