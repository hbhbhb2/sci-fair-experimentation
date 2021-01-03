# control: what pytesseract (the OCR software) perceives the image says

from PIL import Image
import pytesseract
import sys

img = Image.open(sys.argv[1])
retstr = pytesseract.image_to_string(img)

print(retstr)