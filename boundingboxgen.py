# DEBUG SCRIPT
# shows what pytesseract views as the bounding boxes

from PIL import Image, ImageDraw
import pytesseract
import re
import sys
from pathlib import Path

def valid_chr(c: str) -> bool:
    return bool(re.match(c, r"[a-zA-Z\-]"))

path = Path('archive/' + sys.argv[0])
img = Image.open(path) # python3 boundingboxgen.py [path]
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
img.show()
