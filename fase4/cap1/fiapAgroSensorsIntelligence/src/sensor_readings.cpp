#include "sensor_readings.h"
#include "pins.h"

#define DHTTYPE DHT22

SensorReadings::SensorReadings() {
    dht = new DHT(DHT_PIN, DHTTYPE);
}

void SensorReadings::begin() {
    dht->begin();
}

float SensorReadings::mapToPercent(int rawValue) {
    return (rawValue / 4095.0) * 100.0;
}

float SensorReadings::mapToPH(int rawValue) {
    return (rawValue / 4095.0) * 14.0;
}

float SensorReadings::getSoilMoisture() {
    return mapToPercent(analogRead(SOIL_MOISTURE_PIN));
}

float SensorReadings::getPH() {
    return mapToPH(analogRead(PH_SENSOR_PIN));
}

float SensorReadings::getNutrients() {
    return mapToPercent(analogRead(NUTRIENTS_PIN));
}

float SensorReadings::getLuminosity() {
    return mapToPercent(analogRead(LDR_PIN));
}

float SensorReadings::getTemperature() {
    return dht->readTemperature();
}

float SensorReadings::getAirHumidity() {
    return dht->readHumidity();
}