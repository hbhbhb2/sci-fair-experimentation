from PIL import Image, ImageDraw
import pytesseract
import re

def valid_chr(c):
    return bool(re.match(c, r"[a-zA-Z\-]"))

img = Image.open('archive/test_v2/test/TEST_0009.jpg')
imgdraw = ImageDraw.Draw(img)

# this fn returns lines of:
# [guessed char] [x1] [y1 from bottom] [x2] [y2 from bottom] 0
c = pytesseract.image_to_boxes(img) 
print(c)

# separate for processing
l = [line.split(" ") for line in c.splitlines()]

for line in l:
    coords = [
        (int(line[1]), img.size[1] - int(line[2])),
        (int(line[3]), img.size[1] - int(line[4]))
    ] # [(x1, y1), (x2, y2)]
    
    imgdraw.rectangle(coords, outline="red")
