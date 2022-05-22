
// -----
// SimplePollRotatorLCD.ino - Example for the RotaryEncoder library.
// This class is implemented for use with the Arduino environment.
// Copyright (c) by Matthias Hertel, http://www.mathertel.de
// This work is licensed under a BSD style license. See http://www.mathertel.de/License.aspx
// More information on: http://www.mathertel.de/Arduino
// -----
// 18.01.2014 created by Matthias Hertel
// -----

// This example checks the state of the rotary encoder in the loop() function.
// The current position is printed on output when changed.

// Hardware setup:
// Attach a rotary encoder with output pins to A2 and A3.
// The common contact should be attached to ground.

#include <Wire.h>
#include <cmath>
#include <RotaryEncoder.h>
#include "Throttle.h"

#define PIN_IN1 1
#define PIN_IN2 0
#define deadzone 0
#define Rightoffset 30

int previoussteeringDifRight = 0;
int previoussteeringDifLeft = 0;
double throttleVolts = 0;
uint8_t throttleOut = 0;

int steeringDifRight = 0;
int steeringDifLeft = 0;

// teensy analog voltage testing for throttle
unsigned int count = 0;
Throttle throttle(0.1, 0.01);

// dir indicates direction of actuator movement
void WriteToLinearRight(int dir, int pwm)
{
    pwm = pwm * 50;
    // if(pwm < 130){
    //   pwm = 0;
    // }
    // if(dir < 4){
    //   dir = 0;
    // }

    // analogWrite(3, min(255, dir * 30)); // direction of actuator movement
    // analogWrite(4, min(255, pwm));      // speed of movement
    // pins are 3 and 4
}

void WriteToLinearLeft(int dir, int pwm)
{
    pwm = pwm * 50;
    // if(pwm < 130){
    //   pwm = 0;
    // }
    // if(dir < 4){
    //   dir = 0;
    // }

    // analogWrite(12, min(255, dir * 30));
    // analogWrite(16, min(255, pwm));
    // pins are 3 and 4
}

// Setup a RotaryEncoder with 2 steps per latch for the 2 signal input pins:
RotaryEncoder encoder(PIN_IN1, PIN_IN2, RotaryEncoder::LatchMode::TWO03);

void setup()
{
    Serial.begin(9600); // setup()
    Serial2.begin(9600);
}

// Read the current position of the encoder and print out when changed.
void loop()
{
    delay(10);

    static int pos = 0;
    static int throttleVal = 0;
    encoder.tick();
    throttle.update();

    // int newPos = encoder.getPosition();
    // if (pos != newPos)
    // {

    //     // Serial.println(newPos);
    //     pos = newPos;
    // }

    // READ FROM PICO HERE

    if (Serial2.available())
    {
        Serial.println(Serial2.readStringUntil('\n'));

        // int in = Serial2.readStringUntil('\n').toInt();
        // Serial.println(in);
        // pos = in / 1000;               // get first 3 digits
        // throttleVal = in - pos * 1000; // get last 3 digits
        // pos -= 150;
        // throttleVal -= 150;
    }

    // Serial.println(String(pos) + ", " + String(throttleVal));

    // MANUAL THROTTLE CONTROL

    // if (count == 1000)
    // {
    //     count = 0;
    //     if (throttle.getVolts() < 1.5)
    //     {
    //         throttle.setVolts(3);
    //     }
    //     else
    //     {
    //         throttle.setVolts(1);
    //     }
    // }

    // throttleVolts = doubleMap(throttleVal, 0, 300, 0.1, 3.3);

    // Serial.println(String(throttle.getSetPoint()) + ", " + String(throttle.getVal()) + ", " + String(throttle.getVolts()));

    analogWrite(A14, throttle.getVal());

    // Serial.println(String(pos) + ", " + String(throttle));
    //  correct so that 0 is no steering

    // if (Serial2 > 0)
    // {
    //     int incomingCommand =

    //     Serial.print("Serial received: ");
    //     Serial.println(incomingCommand);

    //     // int steering = round(incomingCommand / 1000); // get first three digits

    //     // pos = steering - 150; // convert 0-300 to -150-150
    // }

    pos = min(pos, 150);
    pos = max(-150, pos);

    int LinearActuatorRight = analogRead(A7); // current position of actuators
    int LinearActuatorLeft = analogRead(A5);

    steeringDifRight = LinearActuatorRight - 2 * pos - 354 + Rightoffset;             // get difference between current position and desired of actuators
    steeringDifRight = (previoussteeringDifRight * 1.5 + steeringDifRight * 0.5) / 2; // rolling average with previous positions

    steeringDifLeft = LinearActuatorLeft + 2 * pos - 354;
    steeringDifLeft = (previoussteeringDifLeft * 1.5 + steeringDifLeft * 0.5) / 2;

    // Serial.println("Linear acuatorRight: " + String(LinearActuatorRight) + " Steering DifRight: " + String(steeringDifRight) + " LinearActuatorRight - steeringDifRight: " + String(LinearActuatorRight - steeringDifRight));

    WriteToLinearRight(0, 100); // 0 is back, 255 is out
    if (LinearActuatorRight - steeringDifRight > 50 && LinearActuatorRight - steeringDifRight < 620)
    {
        if (steeringDifRight > 0)
        {
            if (steeringDifRight < deadzone)
                steeringDifRight = 0;
            WriteToLinearRight(0, steeringDifRight);
        }
        else
        {
            if (steeringDifRight > -deadzone)
                steeringDifRight = 0;
            WriteToLinearRight(255, -steeringDifRight);
        }
    }

    if (LinearActuatorLeft - steeringDifLeft > 240 && LinearActuatorLeft - steeringDifLeft < 480)
    {
        if (steeringDifLeft > 0)
        {
            if (steeringDifLeft < deadzone)
                steeringDifLeft = 0;
            WriteToLinearLeft(0, steeringDifLeft);
        }
        else
        {
            if (steeringDifLeft > -deadzone)
                steeringDifLeft = 0;
            // WriteToLinearLeft(255, -steeringDifLeft);
        }
    }

    previoussteeringDifRight = steeringDifRight;
    previoussteeringDifLeft = steeringDifLeft;

    count++;
}

// The End
