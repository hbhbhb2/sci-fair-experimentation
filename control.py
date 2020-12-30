# control: what pytesseract (the OCR software) perceives the image says

from PIL import Image
import pytesseract

img = Image.open('TEST.jpg')
retstr = pytesseract.image_to_string(img)

print(retstr)