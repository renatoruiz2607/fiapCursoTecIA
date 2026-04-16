#pragma once

int countActiveNutrients(
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk
);

bool shouldBlockIrrigationByRain(
  int rainForecastLevel
);

bool shouldTurnWaterPumpOn(
  int rainForecastLevel,
  int rModelIrrigationDecision,
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
  int rModelIrrigationDecision,
  float soilMoisture,
  float temperature,
  float phValue,
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk
);