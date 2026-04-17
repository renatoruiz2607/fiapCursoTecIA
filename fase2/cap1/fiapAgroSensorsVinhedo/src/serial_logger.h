#pragma once

void printSystemHeader();

void printWeatherStatus(
  const char* weatherCity,
  int rainForecastLevel,
  const char* rainForecastText,
  float maxRainProbabilityPercent,
  float maxRainVolumeMm
);

void printRModelStatus(
  const char* rModelMode,
  float modelSoilMoisture,
  float modelPhValue,
  int modelActiveNutrients,
  int modelPotassiumOk,
  int modelRainForecastLevel,
  float irrigationProbability,
  const char* irrigationText
);

void printNpkStatus(
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk,
  int activeNutrients
);

void printPhStatus(
  int phRawValue,
  float phValue
);

void printSoilMoistureStatus(
  float soilMoisture,
  float temperature
);

void printIrrigationDecision(
  int rainForecastLevel,
  int rModelIrrigationDecision,
  float soilMoisture,
  float temperature,
  float phValue,
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk
);

void printWaterPumpStatus(
  bool waterPumpOn
);