#include <Arduino.h>

#include "constants.h"
#include "pins.h"
#include "sensor_readings.h"
#include "irrigation_logic.h"
#include "serial_logger.h"
#include "weather_input.h"
#include "r_model_input.h"

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
  initializeRModelInput();

  delay(200);

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

  Serial.println("Starting smart irrigation system for grapevine...");
  Serial.println();
}

// ============================
// HANDLE SERIAL INPUTS
// ============================

void handleSerialInput() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    // WEATHER INPUT
    if (input == "0") {
      setRainForecastLevel(0);
    } else if (input == "1") {
      setRainForecastLevel(1);
    }

    // R MODEL INPUT
    else if (input == "r0") {
      setRModelManualDecision(0);
    } else if (input == "r1") {
      setRModelManualDecision(1);
    } else if (input == "ra") {
      resetRModelToAuto();
    }
  }
}

// ============================
// LOOP
// ============================

void loop() {
  // updateRainForecastFromSerial();
  // updateRModelInputFromSerial();
  handleSerialInput();

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
  int rModelIrrigationDecision = getRModelIrrigationDecision();

  updateWaterPumpState(
    waterPumpOn,
    rainForecastLevel,
    rModelIrrigationDecision,
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

  printSystemHeader();

  printWeatherStatus(
    getWeatherCity(),
    rainForecastLevel,
    getRainForecastText(),
    getMaxRainProbabilityPercent(),
    getMaxRainVolumeMm()
  );

  printRModelStatus(
    getRModelMode(),
    getRModelSoilMoisture(),
    getRModelPhValue(),
    getRModelActiveNutrients(),
    getRModelPotassiumOk(),
    getRModelRainForecastLevel(),
    getRModelIrrigationProbability(),
    getRModelIrrigationText()
  );

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
    rModelIrrigationDecision,
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