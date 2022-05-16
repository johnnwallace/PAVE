from machine import I2C
from hmc5883l import HMC5883L
from time import sleep
from bn880 import BN880
from humPro import humPro
# Please check that correct PINs are set on hmc5883l library!
rf = humPro(
    crespPin=27, bePin=21, cmdPin=26, ctsPin=22, txPin=16, rxPin=17, modeIndPin=18
)
BUTTON = machine.Pin(14, machine.Pin.IN,machine.Pin.PULL_DOWN)  # button pin

txPin = machine.Pin(4)
rxPin = machine.Pin(5)
uart = machine.UART(1, 9600, tx=txPin, rx=rxPin) # uart to teensy

#BUTTON.irq(trigger=Pin.IRQ_RISING, handler=rf.transmitRandNumber)
#rf.CRESP.irq(trigger=Pin.IRQ_RISING, handler=rf.readData)

pos = 150
throttle = 150

led = machine.Pin(25, machine.Pin.OUT)  

# sleep(3)

while True:
    sleep(0.1)
    
    strIn = rf.readData()
    
    if strIn is not None:
        strIn = strIn.decode('utf-8')
        if strIn == "w\n":
            throttle += 1
        if strIn == "s\n":
            throttle -= 1
        if strIn == "a\n":
            pos += 1
        if strIn == "d\n":
            pos -= 1
            
    strOut = str(pos) + str(throttle) + '\n'
    uart.write(strOut)
    print(strOut)
    
    led.toggle()