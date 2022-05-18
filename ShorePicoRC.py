from machine import I2C
from time import sleep
from humPro import humPro
import uselect
import sys

rf = humPro(
    crespPin=27, bePin=21, cmdPin=26, ctsPin=22, txPin=16, rxPin=17, modeIndPin=18
)

rollingData = ""

while True:
    list = uselect.select([sys.stdin], [], [], 0.01)

    if list[0]:
        byte = sys.stdin.read(1)
        rf.transmitData(byte)
    else:
        byte = None

    packet = rf.readData()
    if packet is not None:
        packetStr = packet.decode("utf-8")

        start = packetStr.find("x")
        if start != -1:
            rollingData += packetStr[
                0 : start - 1
            ]  # append all characters before start character
            thisData = rollingData.split()  # split rollingData to get data
            rollingData = packetStr[
                start + 1 :
            ]  # reset rollingData to the characters after the start character
        else:
            rollingData += packetStr
