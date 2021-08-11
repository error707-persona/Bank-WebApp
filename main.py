# for tracking muse
import time

import win32api
while True:
    a = win32api.GetKeyState(0x01)
    if a<0:
        print("left click!")
    time.sleep(0.3)