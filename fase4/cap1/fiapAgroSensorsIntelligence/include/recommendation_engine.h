#pragma once

#include <Arduino.h>

class RecommendationEngine {
public:
    String generateRecommendation(
        float soilMoisture,
        float ph,
        float nutrientsLevel,
        float temperature,
        float airHumidity,
        float productivityIndex
    );

private:
    bool isSoilMoistureCritical(float soilMoisture);
    bool isSoilMoistureLow(float soilMoisture);
    bool isPhAdequate(float ph);
    bool isNutrientsLevelAdequate(float nutrientsLevel);
    bool hasHighEvaporationRisk(float temperature, float airHumidity);
};