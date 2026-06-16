#include "productivity_engine.h"

float ProductivityEngine::calculateProductivityIndex(
    float soilMoisture,
    float ph,
    float luminosity,
    float nutrientsLevel
) {
    float soilMoistureScore = calculateSoilMoistureScore(soilMoisture);
    float phScore = calculatePhScore(ph);
    float luminosityScore = calculateLuminosityScore(luminosity);
    float nutrientsScore = calculateNutrientsScore(nutrientsLevel);

    float productivityIndex = (
        soilMoistureScore +
        phScore +
        luminosityScore +
        nutrientsScore
    ) / 4.0;

    return limitScore(productivityIndex);
}

String ProductivityEngine::classifyProductivity(float productivityIndex) {
    if (productivityIndex < 40.0) {
        return "Baixa";
    }

    if (productivityIndex < 70.0) {
        return "Moderada";
    }

    return "Alta";
}

float ProductivityEngine::calculateSoilMoistureScore(float soilMoisture) {
    if (soilMoisture >= 60.0 && soilMoisture <= 80.0) {
        return 100.0;
    }

    if (soilMoisture >= 45.0 && soilMoisture < 60.0) {
        return 75.0;
    }

    if (soilMoisture > 80.0 && soilMoisture <= 90.0) {
        return 70.0;
    }

    if (soilMoisture >= 30.0 && soilMoisture < 45.0) {
        return 45.0;
    }

    if (soilMoisture > 90.0) {
        return 30.0;
    }

    return 20.0;
}

float ProductivityEngine::calculatePhScore(float ph) {
    if (ph >= 5.5 && ph <= 7.0) {
        return 100.0;
    }

    if (ph >= 5.0 && ph < 5.5) {
        return 70.0;
    }

    if (ph > 7.0 && ph <= 7.5) {
        return 70.0;
    }

    if (ph >= 4.5 && ph < 5.0) {
        return 40.0;
    }

    if (ph > 7.5 && ph <= 8.0) {
        return 40.0;
    }

    return 20.0;
}

float ProductivityEngine::calculateLuminosityScore(float luminosity) {
    if (luminosity >= 50.0 && luminosity <= 85.0) {
        return 100.0;
    }

    if (luminosity >= 35.0 && luminosity < 50.0) {
        return 75.0;
    }

    if (luminosity > 85.0 && luminosity <= 95.0) {
        return 70.0;
    }

    if (luminosity >= 20.0 && luminosity < 35.0) {
        return 45.0;
    }

    if (luminosity > 95.0) {
        return 55.0;
    }

    return 20.0;
}

float ProductivityEngine::calculateNutrientsScore(float nutrientsLevel) {
    return limitScore(nutrientsLevel);
}

float ProductivityEngine::limitScore(float value) {
    if (value < 0.0) {
        return 0.0;
    }

    if (value > 100.0) {
        return 100.0;
    }

    return value;
}