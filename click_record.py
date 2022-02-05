import pyautogui
import sys
print('Press Ctrl-C to quit.')
try:
    positionStr = ''
    while True:
        x, y = pyautogui.position()
        position = positionStr
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        if position != positionStr:
            print(positionStr)
except KeyboardInterrupt:
    print('\n')
