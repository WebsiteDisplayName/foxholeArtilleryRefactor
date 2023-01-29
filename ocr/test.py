# Mouse location: https://docs.google.com/document/d/1el2fGCOhXFpR9ADOG8K1Ih_GNmPv29dH9NMt0LJZlN4/edit
# Screenshot area


#! python3
import pyautogui
import sys
import keyboard
from PIL import Image
import PIL
import os

import numpy as np
import easyocr
# -50, 0, 100, 100
# small box around cursor screen cap


def screenshotMouseArea(fileName, left=-38, top=14, width=74, height=40):
    # left, top, width, height
    x, y = pyautogui.position()
    positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    print(positionStr, end='')
    print('\b' * len(positionStr), end='', flush=True)

    # adjust coords
    left += x
    top += y

    # file path adjustments
    im = pyautogui.screenshot(region=(left, top, width, height))
    im = im.convert("L")
    script_dir = os.path.dirname(__file__)
    rel_path = "images\\" + fileName + ".png"
    abs_file_path = os.path.join(script_dir, "..", rel_path)
    im.save(abs_file_path)
    return


# https://github.com/boppreh/keyboard#api
# counter = 0
while True:
    keyboard.wait("right alt")
    screenshotMouseArea(f"test{1}")
    # counter += 1


# IMAGE_PATH = '../images/test0.png'
# # Same code here just changing the attribute from ['en'] to ['zh']
# reader = easyocr.Reader(['en'])
# result = reader.readtext(IMAGE_PATH, paragraph="False")
# print(result)
