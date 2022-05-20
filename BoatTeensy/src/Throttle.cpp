#include "Throttle.h"

Throttle::Throttle(double k, double maxChange)
{
    this->k = k;
    this->maxChange = maxChange;
}

// set setPoint to val but restrict to 0-maxVolts
void Throttle::setVolts(double val)
{
    if (val >= maxVolts)
    {
        setPoint = maxVolts;
    }
    else if (val <= 0)
    {
        setPoint = 0;
    }
    else
    {
        setPoint = val;
    }
}

void Throttle::update()
{
    double diff = setPoint - thisVolts;
    double change = diff * k;

    if (abs(diff) < maxChange)
    {
        thisVolts = setPoint;
        return;
    }

    if (change > maxChange)
    {
        thisVolts += maxChange;
    }
    else if (change < -maxChange)
    {
        thisVolts -= maxChange;
    }
    else
    {
        thisVolts += change;
    }
}

uint8_t Throttle::getVal()
{
    return doubleMap(thisVolts, 0, 3.3, 0, 255);
}

double doubleMap(double x, double in_min, double in_max, double out_min, double out_max)
{
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}