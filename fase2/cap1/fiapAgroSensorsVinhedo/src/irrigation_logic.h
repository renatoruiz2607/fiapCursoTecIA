#pragma once

int countActiveNutrients(
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk
);

bool shouldTurnWaterPumpOn(
  int rainForecastLevel,
  float soilMoisture,
  float temperature,
  float phValue,
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk
);

void updateWaterPumpState(
  bool& waterPumpOn,
  int rainForecastLevel,
  float soilMoisture,
  float temperature,
  float phValue,
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk
);

bool shouldBlockIrrigationByRain(
  int rainForecastLevel
);