# creates a csv returning the accuracy between the control & the ai

from ai_guess import guess
from control import control 
from PIL import Image
import os
import shutil
import random
import csv
from pathlib import Path
from typing import List # list[] generics aren't a thing in python 3.8.7 :(
from itertools import tee, zip_longest
import re

PERIODS = 9 # num of periods: [0, X)
SAMPLE_LEN = 10 # num of images per period
BENCHMARK_ROOT = Path("benchmark")
FILENAME_FORMAT = "TEST_{:04d}.jpg" # TEST_XXXX.jpg or TEST_XXXXX.jpg

TEST_PATH = Path('archive/test_v2/test/')
TEST_CSV  = Path('archive/written_name_test_v2.csv')

if not os.path.isdir(TEST_PATH):
    raise FileNotFoundError("Could not find directory at {TEST_PATH}.")
if not os.path.isfile(TEST_CSV):
    raise FileNotFoundError("Could not find file at {TEST_CSV}.")


## create benchmark folder & periods folders

# tries a mkdir. if dir exists, then just ignore
def try_mkdir(path: os.PathLike):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

# get path for a period folder
def period_path(i) -> os.PathLike:
    istr = str(i).rjust(len(str(PERIODS)), "0")
    return os.path.join(BENCHMARK_ROOT, "PERIOD" + istr)

try_mkdir(BENCHMARK_ROOT)
for i in range(PERIODS):
    try_mkdir(period_path(i))

## copy a random set of images into period folder
NUM_FILES = len(os.listdir(TEST_PATH))
file_choices = [os.path.join(TEST_PATH, FILENAME_FORMAT.format(i)) for i in random.sample(range(1, NUM_FILES + 1), PERIODS * SAMPLE_LEN)]

for i in range(PERIODS * SAMPLE_LEN):
    f = file_choices[i]
    shutil.copy(f, period_path(i % PERIODS))

## get control & ai guesses & the correct guess (from csv) for each period
# every n-tuplet (where n = SAMPLE_LEN) sublist = 1 period
control_guesses: List[str] = []
ai_guesses:      List[str] = []
correct_guesses: List[str] = []

def filter_invalidchars(s):
    return re.sub(r"[^A-Z\-']", "", s)
def filter_noms(s):
    if s[:3] == "NOM": s = s[3:]
    if s[:6] == "PRENOM": s = s[6:]
    return s

def filter(s):
    return filter_noms(filter_invalidchars(s))

with open(TEST_CSV) as f:
    reader = csv.reader(f)
    reader_tee = [*tee(reader, PERIODS * SAMPLE_LEN)]

    def get_iden(iter, filename):
        return next(i for n, i in iter if n == filename)

    for period in range(PERIODS):
        period_root = period_path(period)
        period_img_names = os.listdir(period_root)
        period_imgs = [Image.open(os.path.join(period_root, p)) for p in period_img_names]

        control_guesses += [filter(control(img))             for img in period_imgs]
        ai_guesses      += [filter(guess(img, state=period)) for img in period_imgs]

        #inefficient, but basically, whenever the csv is read, iter thru the csv until the right file is found and use that to get the identity
        correct_guesses += [filter(get_iden(reader_tee.pop(), name)) for name in period_img_names]
        pass

print(control_guesses)
print(ai_guesses)
print(correct_guesses)

## calculate accuracies
def accuracy_check(observed: str, correct: str) -> float:
    # ACCURACY CALCULATION
    # 1. Line up characters by index.
    #   ex. HELLO - HAPPY 
    #       (H-H, E-A, L-P, L-P, O-Y)
    # 2. If the characters match, that is considered a correct compare.
    #   ex. HELLO - HAPPY
    #       (there is 1 correct compare)
    # 3. If the length of the words are different, any leftover characters are considered incorrect compares.
    #   ex. HOUSE - MOUSES
    #       (H-M, O-O, U-U, S-S, E-E, _-S)
    #       4 correct compares, 2 incorrect compares
    # 4. Accuracy = correct compares / total compares
    correct_compares = 0
    total_compares = 0

    compare_zips = zip_longest(observed, correct)
    for obchr, crchr in compare_zips:
        total_compares += 1
        if obchr == crchr: correct_compares += 1

    return correct_compares / total_compares

control_accuracy: List[float] = []
ai_accuracy: List[float] = []
for i, correct_guess in enumerate(correct_guesses):
    control_guess = control_guesses[i]
    ai_guess = ai_guesses[i]

    control_accuracy.append(accuracy_check(control_guess, correct_guess))
    ai_accuracy.append(accuracy_check(ai_guess, correct_guess))

## create 2D arrays dividing each period
def div_into_batches(l: List, n: int) -> List[List]:
    # https://stackoverflow.com/a/9671301
    return [l[x:x+n] for x in range(0, len(l), n)]

control_accuracies_per_period = div_into_batches(control_accuracy, SAMPLE_LEN)
ai_accuracies_per_period = div_into_batches(ai_accuracy, SAMPLE_LEN)

## create csvs
with open(os.path.join(BENCHMARK_ROOT, 'control_results.csv'), 'w') as f:
    writer = csv.writer(f)

    writer.writerow(['PERIOD', *("TRIAL " + str(i) for i in range(SAMPLE_LEN)), 'AVERAGE'])
    for period in range(PERIODS):
        period_accuracies = control_accuracies_per_period[period]
        avg = sum(period_accuracies) / len(period_accuracies)
        writer.writerow([period, *period_accuracies, avg])

with open(os.path.join(BENCHMARK_ROOT, 'ai_results.csv'), 'w') as f:
    writer = csv.writer(f)

    writer.writerow(['PERIOD', *("TRIAL " + str(i) for i in range(SAMPLE_LEN)), 'AVERAGE'])
    for period in range(PERIODS):
        period_accuracies = ai_accuracies_per_period[period]
        avg = sum(period_accuracies) / len(period_accuracies)
        writer.writerow([period, *period_accuracies, avg])