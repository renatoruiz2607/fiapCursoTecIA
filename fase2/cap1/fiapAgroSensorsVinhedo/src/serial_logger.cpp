#include <Arduino.h>

#include "constants.h"
#include "irrigation_logic.h"
#include "serial_logger.h"

void printLogTitle() {
    Serial.println("===== AGRO SENSORS VINHEDO =====");
}

void printNpkStatus(
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk,
  int activeNutrients
) {
  Serial.println("===== NPK STATUS =====");

  Serial.print("Nitrogen: ");
  Serial.println(nitrogenLevelOk ? "OK" : "LOW");

  Serial.print("Phosphorus: ");
  Serial.println(phosphorusLevelOk ? "OK" : "LOW");

  Serial.print("Potassium: ");
  Serial.println(potassiumLevelOk ? "OK" : "LOW");

  Serial.print("Active nutrients: ");
  Serial.println(activeNutrients);

  Serial.println("======================");
}

void printPhStatus(
  int phRawValue,
  float phValue
) {
  Serial.println("===== PH SENSOR STATUS =====");

  Serial.print("LDR raw value: ");
  Serial.println(phRawValue);

  Serial.print("Simulated soil pH: ");
  Serial.println(phValue, 2);

  Serial.println("============================");
}

void printSoilMoistureStatus(
  float soilMoisture,
  float temperature
) {
  Serial.println("===== SOIL MOISTURE STATUS =====");

  if (isnan(soilMoisture) || isnan(temperature)) {
    Serial.println("Failed to read from DHT22 sensor.");
  } else {
    Serial.print("Simulated soil moisture: ");
    Serial.print(soilMoisture, 2);
    Serial.println("%");

    Serial.print("Temperature: ");
    Serial.print(temperature, 2);
    Serial.println(" C");
  }

  Serial.println("================================");
}

void printIrrigationDecision(
  float soilMoisture,
  float temperature,
  float phValue,
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk
) {
  Serial.println("===== IRRIGATION DECISION =====");

  if (isnan(soilMoisture) || isnan(temperature)) {
    Serial.println("Decision: OFF");
    Serial.println("Reason: DHT22 reading failed");
  } else if (soilMoisture >= MIN_SOIL_MOISTURE) {
    Serial.println("Decision: OFF");
    Serial.println("Reason: Soil moisture is sufficient");
  } else if (phValue < MIN_PH || phValue > MAX_PH) {
    Serial.println("Decision: OFF");
    Serial.println("Reason: Soil pH is out of ideal range for grapevine");
  } else if (!potassiumLevelOk) {
    Serial.println("Decision: OFF");
    Serial.println("Reason: Potassium level is not adequate");
  } else if (countActiveNutrients(
      nitrogenLevelOk,
      phosphorusLevelOk,
      potassiumLevelOk
    ) < MIN_ACTIVE_NUTRIENTS) {
    Serial.println("Decision: OFF");
    Serial.println("Reason: Minimum nutrient combination not reached");
  } else {
    Serial.println("Decision: ON");
    Serial.println("Reason: All irrigation conditions were satisfied");
  }

  Serial.println("================================");
}

void printWaterPumpStatus(
  bool waterPumpOn
) {
  Serial.println("===== WATER PUMP STATUS =====");
  Serial.print("Water pump: ");
  Serial.println(waterPumpOn ? "ON" : "OFF");
  Serial.println("=============================");
  Serial.println();
}