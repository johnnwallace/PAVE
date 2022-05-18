import numpy as np
from bn880 import BN880
from hmc5883l import HMC5883L
import time

APPROX_LAT = (
    90  # approximate latitude of race, used to convert latitude and longitude to grid
)
RADIUS = 6371  # radius of Earth in km

gps = BN880()
lastTime = time.ticks_ms
thisTime = lastTime

lastX = lastY = 0
lastXVelo = lastYVelo = 0

# https://stackoverflow.com/questions/16266809/convert-from-latitude-longitude-to-x-y#:~:text=latitude%20%3D%20Math.,radius)%20*%20Math.
def toGrid(lat, long):
    x = RADIUS * long * np.cos(APPROX_LAT * np.pi / 180)
    y = RADIUS * APPROX_LAT * np.pi / 180

    return x, y


while True:
    thisTime = time.ticks_ms
    dt = time.ticks_diff(thisTime, lastTime)
    lastTime = thisTime

    [lat, long] = gps.read()
    [thisX, thisY] = toGrid(lat, long)

    xVelo = (thisX - lastX) / dt # x is E/W
    yVelo = (thisY - lastY) / dt # y is N/S

    xAccel = (xVelo - lastXVelo) / dt
    yAccel = (yVelo - lastYVelo) / dt

    lastX = thisX
    lastY = thisY

    heading = np.arcsin(xVelo, yVelo)  # going straight north is 0
