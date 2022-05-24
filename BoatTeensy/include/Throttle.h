#pragma once
#include "Arduino.h"

class Throttle
{

    unsigned static const int pin = A14;

    double k;             // fraction of error that is added to throttle each update step
    double maxChange;     // maximum voltage change in one update step
    double thisVolts = 0; // current voltage
    double setPoint;      // desired voltage output
    double maxVolts = 3.3;

    uint8_t thisValue; // current value written to analog

public:
    Throttle(double k, double maxChange);
    double getVolts() { return thisVolts; }
    double getSetPoint() { return setPoint; }
    void setVolts(double val);
    uint8_t getVal();

    String toString();

    void update();
};

double doubleMap(double x, double in_min, double in_max, double out_min, double out_max);