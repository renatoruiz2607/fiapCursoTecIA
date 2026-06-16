#include "sensor_readings.h"
#include "productivity_engine.h"
#include "recommendation_engine.h"

SensorReadings sensors;
ProductivityEngine productivityEngine;
RecommendationEngine recommendationEngine;

void setup() {
    Serial.begin(115200);
    sensors.begin();
}

void loop() {
    float soilMoisture = sensors.getSoilMoisture();
    float ph = sensors.getPH();
    float nutrientsLevel = sensors.getNutrients();
    float luminosity = sensors.getLuminosity();
    float temperature = sensors.getTemperature();
    float airHumidity = sensors.getAirHumidity();

    float productivityIndex = productivityEngine.calculateProductivityIndex(
        soilMoisture,
        ph,
        luminosity,
        nutrientsLevel
    );

    String productivityClassification =
        productivityEngine.classifyProductivity(productivityIndex);

    String recommendation = recommendationEngine.generateRecommendation(
        soilMoisture,
        ph,
        nutrientsLevel,
        temperature,
        airHumidity,
        productivityIndex
    );

    float irrigationVolume = recommendationEngine.calculateIrrigationVolume(
        soilMoisture,
        ph,
        nutrientsLevel
    );

    String fertilizationNeed =
        recommendationEngine.classifyFertilizationNeed(nutrientsLevel);

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
    Serial.print(airHumidity, 1);

    Serial.print(";productivity_index=");
    Serial.print(productivityIndex, 1);

    Serial.print(";productivity_classification=");
    Serial.print(productivityClassification);

    Serial.print(";recommendation=");
    Serial.print(recommendation);

    Serial.print(";irrigation_volume=");
    Serial.print(irrigationVolume, 1);

    Serial.print(";fertilization_need=");
    Serial.println(fertilizationNeed);

    delay(3000);
}