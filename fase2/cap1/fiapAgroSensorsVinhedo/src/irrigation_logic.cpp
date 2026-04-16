#include <Arduino.h>

#include "pins.h"
#include "constants.h"
#include "irrigation_logic.h"

int countActiveNutrients(
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk
) {
  int activeNutrients = 0;

  if (nitrogenLevelOk) {
    activeNutrients++;
  }

  if (phosphorusLevelOk) {
    activeNutrients++;
  }

  if (potassiumLevelOk) {
    activeNutrients++;
  }

  return activeNutrients;
}

bool shouldTurnWaterPumpOn(
  int rainForecastLevel,
  float soilMoisture,
  float temperature,
  float phValue,
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk
) {
  if (shouldBlockIrrigationByRain(rainForecastLevel)) {
    return false;
  }

  if (isnan(soilMoisture) || isnan(temperature)) {
    return false;
  }

  int activeNutrients = countActiveNutrients(
    nitrogenLevelOk,
    phosphorusLevelOk,
    potassiumLevelOk
  );

  bool isSoilMoistureLow = soilMoisture < MIN_SOIL_MOISTURE;
  bool isPhInRange = phValue >= MIN_PH && phValue <= MAX_PH;
  bool isPotassiumOk = potassiumLevelOk;
  bool hasMinimumActiveNutrients = activeNutrients >= MIN_ACTIVE_NUTRIENTS;

  return isSoilMoistureLow &&
         isPhInRange &&
         isPotassiumOk &&
         hasMinimumActiveNutrients;
}

void updateWaterPumpState(
  bool& waterPumpOn,
  int rainForecastLevel,
  float soilMoisture,
  float temperature,
  float phValue,
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk
) {
  waterPumpOn = shouldTurnWaterPumpOn(
    rainForecastLevel,
    soilMoisture,
    temperature,
    phValue,
    nitrogenLevelOk,
    phosphorusLevelOk,
    potassiumLevelOk
  );

  digitalWrite(WATER_PUMP_RELAY_PIN, waterPumpOn ? HIGH : LOW);
}

bool shouldBlockIrrigationByRain(
  int rainForecastLevel
) {
  return rainForecastLevel == 1;
}