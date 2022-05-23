from machine import I2C
from time import sleep
from humPro import humPro
import uselect
import sys

rf = humPro(
    crespPin=27, bePin=21, cmdPin=26, ctsPin=22, txPin=16, rxPin=17, modeIndPin=18
)

file = open("data.txt", "w").close()
file = open("data.txt", "w")

led = machine.Pin(25, machine.Pin.OUT)

while True:
    sleep(0.1)
    led.toggle()

    list = uselect.select([sys.stdin], [], [], 0.01)

    if list[0]:
        byte = sys.stdin.read(1)
        print(byte)
        rf.transmitData(byte)
    else:
        byte = None

    # rf.readData()
    # out = rf.getData()

    # print(out)
    # file.write(out + "\n")
