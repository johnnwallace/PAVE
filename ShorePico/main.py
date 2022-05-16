from machine import I2C
from time import sleep
from humPro import humPro
import uselect
import sys

rf = humPro(
    crespPin=27, bePin=21, cmdPin=26, ctsPin=22, txPin=16, rxPin=17, modeIndPin=18
)
BUTTON = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)  # button pin

while True:
    list = uselect.select([sys.stdin], [], [], 0.01)

    if list[0]:
        byte = sys.stdin.read(1)
        rf.transmitData(byte)
    else:
        byte = None
