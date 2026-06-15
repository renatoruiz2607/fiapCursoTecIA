#include "sensor_readings.h"

SensorReadings sensors;

void setup() {
    Serial.begin(115200);
    sensors.begin();

    Serial.println("AgroSensorsIntelligence iniciado");
}

void loop() {
    float soilMoisture = sensors.getSoilMoisture();
    float ph = sensors.getPH();
    float nutrientsLevel = sensors.getNutrients();
    float luminosity = sensors.getLuminosity();
    float temperature = sensors.getTemperature();
    float airHumidity = sensors.getAirHumidity();

    Serial.print("soil_moisture=");
    Serial.print(soilMoisture, 1);

    Serial.print(";ph=");
    Serial.print(ph, 1);

    Serial.print(";nutrients_level=");
    Serial.print(nutrientsLevel, 1);

    Serial.print(";luminosity=");
    Serial.print(luminosity, 1);

    Serial.print(";temperature=");
    Serial.print(temperature, 1);

    Serial.print(";air_humidity=");
    Serial.println(airHumidity, 1);

    delay(3000);
}