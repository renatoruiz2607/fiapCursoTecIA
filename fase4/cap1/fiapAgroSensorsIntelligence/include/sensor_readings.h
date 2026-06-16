#pragma once

#include <DHT.h>

class SensorReadings {
public:
    SensorReadings();

    void begin();

    float getSoilMoisture();
    float getPH();
    float getNutrients();
    float getLuminosity();

    float getTemperature();
    float getAirHumidity();

private:
    DHT* dht;

    float mapToPercent(int rawValue);
    float mapToPH(int rawValue);
};