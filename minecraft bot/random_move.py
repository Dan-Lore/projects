import keyboard
import time
import random


def do():
    move = random.choice('wasd')
    keyboard.press(move)
    time.sleep(1)
    keyboard.release(move)


flag = False

while True:
    try:
        if flag:
            do()
        if keyboard.is_pressed(']'):
            exit()
        if keyboard.is_pressed('['):
            flag = not flag
    except:
        break