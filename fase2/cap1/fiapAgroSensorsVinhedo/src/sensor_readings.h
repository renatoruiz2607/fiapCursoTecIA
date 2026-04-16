#pragma once

void initializeSensors();

void readNpkButtons(
  bool& nitrogenLevelOk,
  bool& phosphorusLevelOk,
  bool& potassiumLevelOk
);

float convertLdrToPh(int rawValue);

void readPhSensor(
  int& phRawValue,
  float& phValue
);

void readSoilMoistureSensor(
  float& soilMoisture,
  float& temperature
);