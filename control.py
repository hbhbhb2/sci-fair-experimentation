from PIL import Image
import pytesseract

img = Image.open('TEST.jpg')
print(pytesseract.image_to_string(img))