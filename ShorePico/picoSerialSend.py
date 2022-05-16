from machine import Pin
import time

led = Pin(25, Pin.OUT)
button = Pin(2, Pin.IN, Pin.PULL_DOWN)
txPin = machine.Pin(12)
rxPin = machine.Pin(13)
uart = machine.UART(0, 9600, tx=txPin, rx=rxPin)

pos = 200
throttle = 150
test = "200150\n"

while True:
    string = str(pos) + str(throttle) + '\n'
    if button.value():
        pos = pos + 1
        uart.write(string)
        print(string)
        led.value(1)
        time.sleep(0.1)
    else:
        led.value(0)
