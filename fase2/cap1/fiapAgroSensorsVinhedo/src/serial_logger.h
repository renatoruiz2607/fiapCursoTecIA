#pragma once

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

void printLogTitle();

void printWeatherStatus(
  int rainForecastLevel
);