#include <Arduino.h>
#include <DHT.h>

#include "pins.h"
#include "sensor_readings.h"

#define DHTTYPE DHT22

DHT dht(DHT_SENSOR_PIN, DHTTYPE);

void initializeSensors() {
  pinMode(NITROGEN_BUTTON_PIN, INPUT_PULLUP);
  pinMode(PHOSPHORUS_BUTTON_PIN, INPUT_PULLUP);
  pinMode(POTASSIUM_BUTTON_PIN, INPUT_PULLUP);
  pinMode(PH_SENSOR_PIN, INPUT);

  dht.begin();
}

void readNpkButtons(
  bool& nitrogenLevelOk,
  bool& phosphorusLevelOk,
  bool& potassiumLevelOk
) {
  nitrogenLevelOk = digitalRead(NITROGEN_BUTTON_PIN) == LOW;
  phosphorusLevelOk = digitalRead(PHOSPHORUS_BUTTON_PIN) == LOW;
  potassiumLevelOk = digitalRead(POTASSIUM_BUTTON_PIN) == LOW;
}

float convertLdrToPh(int rawValue) {
  return (rawValue / 4095.0f) * 14.0f;
}

void readPhSensor(
  int& phRawValue,
  float& phValue
) {
  phRawValue = analogRead(PH_SENSOR_PIN);
  phValue = convertLdrToPh(phRawValue);
}

void readSoilMoistureSensor(
  float& soilMoisture,
  float& temperature
) {
  soilMoisture = dht.readHumidity();
  temperature = dht.readTemperature();
}