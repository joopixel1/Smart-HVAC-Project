import digitalio
import board
import time
pin = digitalio.DigitalInOut(board.D13)
pin2 = digitalio.DigitalInOut(board.D9)
pin.direction = digitalio.Direction.OUTPUT
pin2.direction = digitalio.Direction.OUTPUT
while 1:
    pin.value = True
    pin2.value = False
    time.sleep(.5)
    pin.value = False
    pin2.value = True
    time.sleep(.5)