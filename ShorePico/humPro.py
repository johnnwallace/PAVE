from machine import Pin, UART
import random
class humPro:
    def __init__(self, crespPin, bePin, cmdPin, ctsPin, txPin, rxPin, modeIndPin):
        self.CRESP = Pin(crespPin, Pin.IN)  # CRESP pin (FOR INTERRUPT)
        self.BE = Pin(bePin, Pin.IN)  # BE pin (CAN BE READ THROUGH LSTATUS IF NEEDED)
        self.CMD = Pin(cmdPin, Pin.OUT)  # CMD pin
        self.CTS = Pin(ctsPin, Pin.IN)  # CTS pin
        self.TX = Pin(txPin, Pin.OUT)  # TX pin
        self.RX = Pin(rxPin, Pin.IN)  # RX pin
        self.MODE_IND = Pin(modeIndPin, Pin.IN)  # MODE_IND pin
        self.uart = UART(0, 9600, tx=self.TX, rx=self.RX)  # initialize UART
    # used to configure the HumPRO's settings
    def configure(self):
        if self.MODE_IND.value() == 0:
            self.CMD.value(0)
    def transmitData(self, data):
        if self.CTS.value() == 0:
            self.CMD.value(1)
            self.uart.write(str(data) + "\n")  # prints a line of data to HumPRO
            self.CMD.value(0)
        # hold until HumPRO buffer is empty, indicating all data has been transmitted
        while True:
            if self.BE.value() == 1:
                # ADD EEXFLAG REGISTER SAMPLING HERE --> RETURN TRUE IF NO ERRORS, FALSE IF ERRORS
                return
    # used to read data from the uart connection with the HumPRO
    def readData(self):
        return self.uart.readline()
    def transmitRandNumber(self):
        num = self.generateRandom()
        self.transmitData(num)
        print("sending " + str(num))
    def generateRandom(self):
        num = 0
        for i in range(10):
            num += random.randint(0, 9)
            num * 10
        return num
    def transmitCommands(self, commandString, waypoint):
        string = str(commandString) + " " + str(waypoint)
        self.transmitData(string)
    def transmitTelemetry(self, path, position, st):
        string = str(path) + " " + str(position) + " " + str(st)
        self.transmitData(string)