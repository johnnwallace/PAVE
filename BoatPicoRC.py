from machine import I2C
from hmc5883l import HMC5883L
from time import sleep
from bn880 import BN880
from humPro import humPro
import math

# check that correct PINs are set on hmc5883l library
compass = HMC5883L()
gps = BN880()


rf = humPro(
    crespPin=27, bePin=21, cmdPin=26, ctsPin=22, txPin=16, rxPin=17, modeIndPin=18
)

led = machine.Pin(25, machine.Pin.OUT)

sleep(0.5)

file = open("data.txt", "w").close()
file = open("data.txt", "w")

while True:
    sleep(0.1)

    x, y, z = compass.read()
    deg, minutes = compass.heading(x, y)
    heading = (deg + minutes / 60) * math.pi / 180

    lat, long = gps.read()

    formatLat = "%09.5f" % lat
    formatLong = "%010.5f" % long
    formatHeading = "%09.5f" % heading

    strOut = "x" + formatLat + ", " + formatLong + ", " + formatHeading
    # print(strOut)
    file.write(strOut + "\n")
    rf.transmitData(strOut)
