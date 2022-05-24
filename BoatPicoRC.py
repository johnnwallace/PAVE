from machine import I2C
from hmc5883l import HMC5883L
from time import sleep
from bn880 import BN880
from humPro import humPro
import math

DO_TELEM = False

# check that correct PINs are set on hmc5883l library
if DO_TELEM:
    compass = HMC5883L()
    gps = BN880()

rf = humPro(
    crespPin=27, bePin=21, cmdPin=26, ctsPin=22, txPin=16, rxPin=17, modeIndPin=18
)

txPin = machine.Pin(4)
rxPin = machine.Pin(5)
uart = machine.UART(1, 9600, tx=txPin, rx=rxPin)

led = machine.Pin(25, machine.Pin.OUT)

sleep(0.5)

steering = 150
throttle = 150

count = 0

while True:
    sleep(0.1)
    led.toggle()

    byteIn = rf.readPacket()
    count += 1
    # print(count)

    if byteIn is not None:
        strIn = byteIn.decode("utf-8").replace("\n", "")
        # print(strIn)

        if strIn == "w":
            if throttle < 300:
                throttle += 1
            # print("Increase throttle")
        elif strIn == "s":
            if throttle > 0:
                throttle -= 1
            # print("Deacrease throttle")
        elif strIn == "a":
            if steering < 300:
                steering += 1
            # print("Steer left")
        elif strIn == "d":
            if steering > 0:
                steering -= 1
            # print("Steer right")
        elif strIn == "x":
            steering = 150
            # print("Reset steering")
        elif strIn == "c":
            throttle = 0
            # print("Reset throttle")
        elif strIn == "p":
            throttle = 0
            steering = 150

        # if strIn != '\n': print(strIn)

    if steering < 0:
        steering = 0
    if throttle < 0:
        throttle = 0

    steeringFormat = "%03d" % steering
    throttleFormat = "%03d" % throttle

    strControl = steeringFormat + throttleFormat
    # uart.write(strControl+'\n')
    print(strControl)

    if DO_TELEM:
        x, y, z = compass.read()
        deg, minutes = compass.heading(x, y)
        heading = (deg + minutes / 60) * math.pi / 180

        lat, long = gps.read()

        formatLat = "%09.5f" % lat
        formatLong = "%010.5f" % long
        formatHeading = "%09.5f" % heading

        strOut = "x" + formatLat + ", " + formatLong + ", " + formatHeading
        # print(strOut)
        rf.transmitData(strOut)
