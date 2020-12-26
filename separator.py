from PIL import Image
import pytesseract
import re

def valid_chr(c):
    return bool(re.match(r"[a-zA-Z\-]", c))

def flatten(l):
    return [e for sl in l for e in sl]
img = Image.open('archive/test_v2/test/TEST_0009.jpg')

# this fn returns lines of:
# [guessed char] [x1] [y1 from bottom] [x2] [y2 from bottom] 0
c = pytesseract.image_to_boxes(img)

# separate for processing
l = [line.split(" ") for line in c.splitlines()]

# filter out lines we do not want
filtered = [line for line in l if valid_chr(line[0])]

#check first 3 for "NOM"
if ''.join(line[0] for line in filtered[:3]).upper() == "NOM":
    filtered = filtered[3:]

for i, line in enumerate(filtered):
    # ((x1, y1), (x2, y2))
    coords = (
        (int(line[1]), img.size[1] - int(line[2])),
        (int(line[3]), img.size[1] - int(line[4]))
    )

    # ((lowest x, highest x), (lowest y, highest y))
    bounds = tuple((min(c1, c2), max(c1, c2)) for c1, c2 in zip(*coords))
    # (low x, low y, high x, high y)
    bounds = flatten(zip(*bounds))
    print(bounds)
    img.crop(bounds).save("out/" + str(i) + ".jpg", "JPEG")
    
