# add CommonFiles to import path
import sys

sys.path.insert(1, "CommonFiles")

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pid import PIDController as PID
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from math import atan2
import math
from scipy import spatial

"""Assumptions made: kp, di, kd, ks, dt, tf, setpoint, v, maxMotorAngle, minTurnRadius, external forces, motor angle stays constant"""


class Boat:
    def __init__(
        self,
        x,
        y,
        theta,
        speed,
        angularSpeed,
        motorAngle,
        maxMotorAngle,
        motorTurnRate,
        minTurnRadius,
    ):
        self.x = x
        self.y = y
        self.theta = theta
        self.speed = speed
        self.angularSpeed = angularSpeed
        self.motorAngle = motorAngle

        self.maxMotorAngle = maxMotorAngle  # degrees
        self.motorTurnRate = motorTurnRate  # degrees/ sec PROB WRONG
        self.minTurnRadius = minTurnRadius  # meters (~20 ft)

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

    # Assume linear relationship between motorAngle and turnRadius / orientationChange
    def updateStates(self, dt):
        ds = self.speed * dt
        maxAngularSpeed = (360 * self.speed) / (2 * np.pi * self.minTurnRadius)

        k = 0.75  # To be tuned
        changeAngularSpeed = -k * self.motorAngle * dt
        if np.abs(self.angularSpeed + changeAngularSpeed) < maxAngularSpeed:
            self.angularSpeed += changeAngularSpeed
        else:
            self.angularSpeed = np.sign(self.angularSpeed) * maxAngularSpeed

        dtheta = self.angularSpeed * dt
        dx = ds * np.cos(np.radians(self.theta))
        dy = ds * np.sin(np.radians(self.theta))

        self.x += dx
        self.y += dy
        self.theta += dtheta

    # Assumption: Motor Angle can only be changed at a constant rate
    def changeMotorAngle(self, targetAngle):
        change = targetAngle - self.motorAngle
        if np.abs(change) > motorTurnRate * dt:
            change = np.sign(change) * motorTurnRate * dt

        if np.abs(self.motorAngle + change) > self.maxMotorAngle:
            self.motorAngle = np.sign(self.motorAngle) * self.maxMotorAngle
        else:
            self.motorAngle += change

    # Instantaneous motor change
    def setMotorAngle(self, newMotorAngle):
        if np.abs(newMotorAngle) > self.maxMotorAngle:
            self.motorAngle = np.sign(newMotorAngle) * self.maxMotorAngle
        else:
            self.motorAngle = newMotorAngle


#### GET HEADINGS (FROM LOUIS'S CODE) ----------------------------------------------------------------------------


def get_dist(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


# gives angle between two points with 0 being north
def get_angle(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return math.atan2(dx, dy)


def connect_two(start, end, end_angle, velocity):

    max_angle_change = np.radians(velocity / 10)
    end_angle += np.pi  # accounts for bug in code

    # Get second to last point
    lx = end[0]
    ly = end[1]

    dx = -velocity * np.sin(end_angle)
    dy = -velocity * np.cos(end_angle)

    # calculate second to last point (slpoint)
    slx = lx + dx
    sly = ly + dy
    slpoint = np.array([slx, sly])

    path = []
    path.append(end)
    path.append(slpoint)

    while get_dist(path[-1], start) > 5:
        prev_angle = get_angle(path[-2], path[-1])
        current_x = path[-1][0]
        current_y = path[-1][1]
        next_point = 0
        best_dist = math.inf
        best_angle = 0
        for potential_angle in np.arange(-2, 3):
            potential_angle = np.radians(potential_angle)
            dx = velocity * np.sin(prev_angle + potential_angle)
            dy = velocity * np.cos(prev_angle + potential_angle)
            next_x = current_x + dx
            next_y = current_y + dy
            new_point = np.array([next_x, next_y])
            new_dist = get_dist(new_point, start)
            if new_dist < best_dist:
                best_dist = new_dist
                best_angle = potential_angle
                next_point = new_point
        path.append(next_point)

    start_angle = get_angle(path[-2], path[-1])

    return np.array(path), start_angle


velocity = 5
starting_point = np.array([-500, 0])
start_angle = np.radians(30)
buoys = [
    np.array([1000, 2000]),
    np.array([-1000, 1000]),
    np.array([150, 10]),
    np.array([400, -300]),
]


def get_full_path(current_location, current_heading, max_velocity, waypoints):
    paths = []
    for i, waypoint in enumerate(waypoints):
        if i == 0:
            temp_path, angle = connect_two(
                waypoint, current_location, current_heading, max_velocity
            )
        else:
            temp_path, angle = connect_two(
                waypoints[i], waypoints[i - 1], current_heading, max_velocity
            )
        paths.append(temp_path)
        current_heading = angle
    return paths


paths = get_full_path(starting_point, start_angle, velocity, buoys)


# gives angle between two points with 0 being north
def get_angle_pid(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return math.atan(dy / dx)


paths = np.concatenate(paths)

headings = np.array([])
for i, point in enumerate(paths[:-1]):
    angle = get_angle(paths[i], paths[i + 1])
    if i > 0 and np.abs(angle - headings[-1]) > 2:
        angle -= 2 * np.pi
    headings = np.append(headings, angle)

# convert to degs
for i, angle in enumerate(headings):
    headings[i] = np.degrees(angle)


## RUN SIMULATION (DAVID AND WILL'S CODE) ----------------------------------------------------------------------------

# All in seconds
t = 0
t1 = 50  # change setpoint at t1
tf = 100
dt = 0.01

# Assumptions
maxMotorAngle = 1000  # degrees
motorTurnRate = 45  # degrees/ sec PROB WRONG
minTurnRadius = 0.00001  # meters (~20 ft)

# TO BE TUNED
kp = 2
ki = 0.2
kd = 3
ks = 1

# Initial Boat State Variables
init_x = 0  # meters
init_y = 0  # meters
init_theta = 0.0  # orientation of boat: degrees from east (positive is ccw)
init_speed = 3  # m/s (constant velocity for now until auto throttle is added)
init_angularSpeed = 0  # deg/s
init_motorAngle = 0  # degrees from longitudinal axis of boat (positive is ccw)

# arrays for graph
thetaHistory = init_theta
xHistory = np.array(init_x)
yHistory = np.array(init_y)
speedHistory = np.array(init_speed)
errorHistory = np.array(0)
motorAngleHistory = np.array(init_motorAngle)

boat = Boat(
    init_x,
    init_y,
    init_theta,
    init_speed,
    init_angularSpeed,
    init_motorAngle,
    maxMotorAngle,
    motorTurnRate,
    minTurnRadius,
)

controller = PID(0, kp, ki, kd, ks, maxMotorAngle)

for heading in headings:
    controller.updateSetpoint(heading)

    controller.updateError(boat.getTheta(), dt)
    errorHistory = np.append(errorHistory, controller.getError())

    targetAngle = controller.evaluate()
    boat.setMotorAngle(-targetAngle)
    motorAngleHistory = np.append(motorAngleHistory, boat.getMotorAngle())
    boat.updateStates(dt)

    thetaHistory = np.append(thetaHistory, boat.getTheta())
    xHistory = np.append(xHistory, boat.getX())
    yHistory = np.append(yHistory, boat.getY())
    speedHistory = np.append(speedHistory, boat.getSpeed())
    t += dt

print(t)

time_fit = np.linspace(0, t, num=int(t / dt))  # Time axis
thetaHistory = thetaHistory[:-2].transpose()  # Turn thetaHistory into a row vector
fig, axs = plt.subplots(3, 3)
axs[0, 0].plot(time_fit, thetaHistory)
axs[0, 0].set_title("Steering PID Simulation Orientation")

axs[1, 0].plot(xHistory, yHistory)
axs[1, 0].set_title("Steering PID Simulation (x,y) Coords")

axs[0, 1].plot(time_fit, xHistory[:-2])
axs[0, 1].set_title("x vs t")

axs[1, 1].plot(time_fit, yHistory[:-2])
axs[1, 1].set_title("y vs t")

axs[0, 2].plot(time_fit, motorAngleHistory[:-2])
axs[0, 2].set_title("motor angle vs. t")

axs[1, 2].plot(time_fit, errorHistory[:-2])
axs[1, 2].set_title("error vs. t")

axs[2, 0].plot(time_fit, headings[:-1])
axs[2, 0].set_title("heading vs. t")

plt.show()
