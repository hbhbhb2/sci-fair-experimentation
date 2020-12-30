# separate_img takes an image, separates into characters, returns that list of images

from PIL import Image
import pytesseract
import re

def valid_chr(c: str) -> bool:
    return bool(re.match(r"[a-zA-Z\-]", c))

def flatten(l: list) -> list:
    # https://stackoverflow.com/a/11264751
    return [e for sl in l for e in sl]

def separate_img(img: Image.Image) -> list[Image.Image]:
    # image_to_boxes returns lines of:
    # [guessed char] [x1] [y1 from bottom] [x2] [y2 from bottom] 0
    c = pytesseract.image_to_boxes(img)

    # separate for processing
    l = [line.split(" ") for line in c.splitlines()]

    # filter out lines we do not want
    filtered = [line for line in l if valid_chr(line[0])]

    #check first 3 for "NOM", or first 6 as "PRENOM"
    if ''.join(line[0] for line in filtered[:3]).upper() == "NOM":
        filtered = filtered[3:]
    if ''.join(line[0] for line in filtered[:6]).upper() == "PRENOM":
        filtered = filtered[6:]

    imgs = []
    for line in filtered:
        # ((x1, y1), (x2, y2))
        coords = (
            (int(line[1]), img.size[1] - int(line[2])),
            (int(line[3]), img.size[1] - int(line[4]))
        )

        # ((lowest x, highest x), (lowest y, highest y))
        bounds = tuple((min(c1, c2), max(c1, c2)) for c1, c2 in zip(*coords))
        # (low x, low y, high x, high y)
        bounds = flatten(zip(*bounds))
        imgs.append(img.crop(bounds))
    return imgs

