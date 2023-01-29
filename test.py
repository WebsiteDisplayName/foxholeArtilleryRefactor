# Mouse location: https://docs.google.com/document/d/1el2fGCOhXFpR9ADOG8K1Ih_GNmPv29dH9NMt0LJZlN4/edit
# Screenshot area




#! python3
import pyautogui
import sys
import keyboard
import PIL
import os

# -50, 0, 100, 100
# small box around cursor
def screenshotMouseArea(fileName, left = -50, top = 0, width = 100, height = 100):
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
    script_dir = os.path.dirname(__file__)
    rel_path = "images\\" + fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    im.save(abs_file_path)

while True:
    if keyboard.is_pressed("right alt"):
        screenshotMouseArea("hehexd.jpg")

