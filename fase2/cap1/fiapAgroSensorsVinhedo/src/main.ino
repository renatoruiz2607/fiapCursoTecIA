#include <Arduino.h>

#include "constants.h"
#include "pins.h"
#include "sensor_readings.h"
#include "irrigation_logic.h"
#include "serial_logger.h"
#include "weather_input.h"

// =====================================
// FIAP Agro Sensors Vinhedo
// NPK Buttons + LDR + DHT22 + Relay
// Smart Irrigation System for Grapevine
// =====================================

// ============================
// GLOBAL VARIABLES
// ============================

bool nitrogenLevelOk = false;
bool phosphorusLevelOk = false;
bool potassiumLevelOk = false;

int phRawValue = 0;
float phValue = 0.0f;

float soilMoisture = 0.0f;
float temperature = 0.0f;

bool waterPumpOn = false;

// ============================
// SETUP
// ============================

void setup() {
  Serial.begin(SERIAL_BAUD_RATE);

  pinMode(WATER_PUMP_RELAY_PIN, OUTPUT);
  digitalWrite(WATER_PUMP_RELAY_PIN, LOW);

  initializeSensors();
  initializeWeatherInput();

  Serial.println("Starting smart irrigation system for grapevine...");
  Serial.println();
}

// ============================
// LOOP
// ============================

void loop() {
  updateRainForecastFromSerial();

  readNpkButtons(
    nitrogenLevelOk,
    phosphorusLevelOk,
    potassiumLevelOk
  );

  readPhSensor(
    phRawValue,
    phValue
  );

  readSoilMoistureSensor(
    soilMoisture,
    temperature
  );

  int rainForecastLevel = getRainForecastLevel();

  updateWaterPumpState(
    waterPumpOn,
    rainForecastLevel,
    soilMoisture,
    temperature,
    phValue,
    nitrogenLevelOk,
    phosphorusLevelOk,
    potassiumLevelOk
  );

  int activeNutrients = countActiveNutrients(
    nitrogenLevelOk,
    phosphorusLevelOk,
    potassiumLevelOk
  );

  printLogTitle();

  printWeatherStatus(rainForecastLevel);

  printNpkStatus(
    nitrogenLevelOk,
    phosphorusLevelOk,
    potassiumLevelOk,
    activeNutrients
  );

  printPhStatus(
    phRawValue,
    phValue
  );

  printSoilMoistureStatus(
    soilMoisture,
    temperature
  );

  printIrrigationDecision(
    rainForecastLevel,
    soilMoisture,
    temperature,
    phValue,
    nitrogenLevelOk,
    phosphorusLevelOk,
    potassiumLevelOk
  );

  printWaterPumpStatus(
    waterPumpOn
  );

  delay(LOOP_DELAY_MS);
}