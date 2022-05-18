import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import bn880
import hmc5883l
import micropyGPS
import humPro


# from steering import PIDController as PID


# basically an underdriven P controller (PID w/o ID) to smoothly change throttle level
class Throttle:
    def __init__(self, k, maxChange):
        self.thisThrottle = self.setPoint = 0
        self.k = k  # fraction of error that is added to throttle each update step
        self.maxChange = maxChange

    def set(self, val):
        self.setPoint = val

    def get(self):
        return self.thisThrottle

    def update(self):
        diff = self.setPoint - self.thisThrottle
        change = diff * self.k

        # if difference is within maxChange no need to ramp
        if abs(diff) < self.maxChange:
            self.thisThrottle = self.setPoint

        # limit change to +-maxChange
        if change > self.maxChange:
            self.thisThrottle += self.maxChange
        elif change < -self.maxChange:
            self.thisThrottle -= self.maxChange
        else:
            self.thisThrottle += change


class Boat:
    def __init__(self, maxMotorAngle, minTurnRadius, gps, compass, rf):
        self.gps = gps
        self.compass = compass
        self.rf = rf

        self.maxMotorAngle = maxMotorAngle  # rads
        self.minTurnRadius = minTurnRadius  # meters (~20 ft)

        self.throttle = self.motorAngle = 0

    def getTheta(self):
        return self.theta

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getSpeed(self):
        return self.speed

    def getMotorAngle(self):
        return self.motorAngle

    # TO DO: poll compass and GPS, return array of data
    def sensorEvent(self):

        return data

    # TO DO: map motor angle in rads to -150 - 150
    def setMotorAngle(self, val):
        if np.abs(val) > self.maxMotorAngle:
            self.motorAngle = np.sign(val) * self.maxMotorAngle
        else:
            self.motorAngle = val

    # TO DO: make this ramp
    def setThrottle(self, val):
        self.throttle = val


def testThrottle():
    fig, ax = plt.subplots(1, 2)

    myThrottle = Throttle(0.1, 1)
    myThrottle.set(10)

    time = np.arange(0, 10, 0.1)
    throttle = np.zeros_like(time)

    for x in range(time.size):
        throttle[x] = myThrottle.get()
        myThrottle.update()

    ax[0].plot(time, throttle)

    myThrottle.set(5)
    time = np.arange(0, 10, 0.1)
    throttle = np.zeros_like(time)

    for x in range(time.size):
        throttle[x] = myThrottle.get()
        myThrottle.update()

    ax[1].plot(time, throttle)

    plt.show()


testThrottle()
