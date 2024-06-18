import keyboard
import pyautogui
import time
import random


def do():
    keyboard.press('w')
    keyboard.press('shift')
    pyautogui.mouseDown()


flag = False
i = 0
while True:
    try:
        if flag and i == 0:
            i += 1
            do()
        if keyboard.is_pressed(']'):
            exit()
        if keyboard.is_pressed('['):
            flag = not flag
    except:
        break