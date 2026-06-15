#include "recommendation_engine.h"

String RecommendationEngine::generateRecommendation(
    float soilMoisture,
    float ph,
    float nutrientsLevel,
    float temperature,
    float airHumidity,
    float productivityIndex
) {
    bool phAdequate = isPhAdequate(ph);
    bool nutrientsAdequate = isNutrientsLevelAdequate(nutrientsLevel);

    if (!phAdequate && !nutrientsAdequate) {
        return "Irrigação bloqueada: corrigir pH e nível de nutrientes.";
    }

    if (!phAdequate) {
        return "Irrigação bloqueada: pH inadequado. Corrigir o solo antes de irrigar.";
    }

    if (!nutrientsAdequate) {
        return "Irrigação bloqueada: nível de nutrientes baixo. Fertilizar antes de irrigar.";
    }

    if (isSoilMoistureCritical(soilMoisture)) {
        return "Irrigação urgente recomendada.";
    }

    if (isSoilMoistureLow(soilMoisture)) {
        if (hasHighEvaporationRisk(temperature, airHumidity)) {
            return "Irrigação preventiva recomendada: risco de ressecamento elevado.";
        }

        return "Irrigação recomendada.";
    }

    if (productivityIndex < 40.0) {
        return "Produtividade baixa: revisar condições agronômicas do cultivo.";
    }

    if (hasHighEvaporationRisk(temperature, airHumidity)) {
        return "Monitorar umidade do solo: temperatura alta e baixa umidade do ar.";
    }

    return "Condições adequadas. Nenhuma ação imediata necessária.";
}

bool RecommendationEngine::isSoilMoistureCritical(float soilMoisture) {
    return soilMoisture < 25.0;
}

bool RecommendationEngine::isSoilMoistureLow(float soilMoisture) {
    return soilMoisture >= 25.0 && soilMoisture < 40.0;
}

bool RecommendationEngine::isPhAdequate(float ph) {
    return ph >= 5.5 && ph <= 7.0;
}

bool RecommendationEngine::isNutrientsLevelAdequate(float nutrientsLevel) {
    return nutrientsLevel >= 50.0;
}

bool RecommendationEngine::hasHighEvaporationRisk(float temperature, float airHumidity) {
    return temperature >= 35.0 && airHumidity <= 35.0;
}