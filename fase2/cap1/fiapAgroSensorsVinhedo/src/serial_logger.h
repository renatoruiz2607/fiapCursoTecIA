#pragma once

void printSystemHeader();

void printWeatherStatus(
  const char* weatherCity,
  int rainForecastLevel,
  const char* rainForecastText,
  float maxRainProbabilityPercent,
  float maxRainVolumeMm
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