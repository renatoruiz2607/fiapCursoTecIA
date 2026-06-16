#pragma once

#include <Arduino.h>

class ProductivityEngine {
public:
    float calculateProductivityIndex(
        float soilMoisture,
        float ph,
        float luminosity,
        float nutrientsLevel
    );

    String classifyProductivity(float productivityIndex);

private:
    float calculateSoilMoistureScore(float soilMoisture);
    float calculatePhScore(float ph);
    float calculateLuminosityScore(float luminosity);
    float calculateNutrientsScore(float nutrientsLevel);
    float limitScore(float value);
};