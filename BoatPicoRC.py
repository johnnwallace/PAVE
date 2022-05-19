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

while True:

    rf.readData()

    out = rf.getData()
    print(out)
    file.write(out + "\n")

    sleep(0.2)
