# this script creates training data that we will use for training the character recognition AI

from separator import separate_img
from pathlib import Path
import os
import csv
from PIL import Image
import re

train = Path('archive/train_v2/train/')
train_csv = Path('archive/written_name_train_v2.csv')

out = Path('out/train/')
out_csv = Path('out/train.csv')

MAX_IMGS_READ = 10000 # amt of images from train data that we're reading
IMG_SIZE = (256, 256)

def has_white_col(img: Image.Image) -> bool:
    PXL_WIDTH = 4   # width of center col we're checking
    WIDTH, HEIGHT = IMG_SIZE # img dims
    BOUNDING_PERCENT = 0.90 # brightness to be considered "white"

    # crop to center column
    center_pxls = img.crop(
        ( (WIDTH - PXL_WIDTH) // 2, 0,
          (WIDTH + PXL_WIDTH) // 2, HEIGHT )
    )

    # check if center column is all white
    # https://stackoverflow.com/a/14041871
    extrema = center_pxls.convert('L').getextrema()
    if all(e > BOUNDING_PERCENT * 255 for e in extrema): return True
    return False

with open(train_csv) as f:
    reader = csv.reader(f)
    next(reader) # skip "filename, identity"

    w = open(out_csv, "w")
    writer = csv.writer(w)
    writer.writerow(["FILENAME", "IDENTITY"])

    i = 0 # N of imgs read
    j = 0 # characters saved counter
    for row in reader:
        pathname, identity = row
        identity_no_spaces = re.sub(r'\s', '', identity)

        # dump images whose identity is not known
        if identity == "UNREADABLE": continue

        path = os.path.join(train, pathname)
        with Image.open(path) as img:
            return_imgs = [rimg.resize(IMG_SIZE) for rimg in separate_img(img)] # sep then resize imgs

            # if amt of chars found != length of identity string, dump input img b/c not sure how to handle
            if len(return_imgs) != len(identity_no_spaces): continue
            # if any of the sep'd chars have a white col, dump input img b/c there's mult chrs in one img
            if any(has_white_col(rimg) for rimg in return_imgs): continue

            #print(path, len(return_imgs), identity)

            ideniter = iter(identity_no_spaces)
            for rimg in return_imgs:
                imgname = f"TRAIN_{str(j).rjust(5, '0')}.jpg"
                writer.writerow([imgname, next(ideniter)])

                return_path = os.path.join(out, imgname)
                rimg.save(return_path, "JPEG")
                j += 1
        i += 1

        if i + 1 >= MAX_IMGS_READ: break #stop reading once we have reached the amt of images we wanted to read

    w.close()