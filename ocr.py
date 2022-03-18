import cv2
import os
import re
import pytesseract
from datetime import datetime

images = []


def estimated(tm, size):
    start = datetime.now() - tm
    print("ETA:", start * (288 - size), flush=True)


folder = "PATH TO THE IMAGES FOLDER"  # For Example: D:/Images/

fn = []


def deEmojify(text):
    regrex_pattern = re.compile(
        pattern="["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "❗"
        "�🥂"
        "@"
        "日"
        "]+",
        flags=re.UNICODE,
    )
    return regrex_pattern.sub(r"", text)


def load_images_from_folder(folder):
    for filename in os.listdir(folder):
        images.append(filename)
    k = 0
    for i in images[10:11]:
        start = datetime.now()
        i = deEmojify(i)
        image = cv2.imread(folder + i, 0)

        blur = cv2.blur(image, (3, 3))

        _, thresh = cv2.threshold(blur, 210, 250, cv2.THRESH_BINARY)

        thresh = cv2.bitwise_not(thresh)

        element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(5, 5))

        erode = cv2.erode(thresh, element, 3)
        cv2.imshow("erode", erode)

        cv2.imshow("img", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(k, pytesseract.image_to_string(erode).strip())

        k += 1
        estimated(start, k)


load_images_from_folder(folder)
