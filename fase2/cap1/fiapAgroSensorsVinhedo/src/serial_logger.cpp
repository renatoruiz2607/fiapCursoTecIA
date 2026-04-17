#include <Arduino.h>

#include "constants.h"
#include "irrigation_logic.h"
#include "serial_logger.h"

void printSystemHeader() {
  Serial.println("===== AGRO SENSORS VINHEDO =====");
}

void printWeatherStatus(
  const char* weatherCity,
  int rainForecastLevel,
  const char* rainForecastText,
  float maxRainProbabilityPercent,
  float maxRainVolumeMm
) {
  Serial.println("===== WEATHER STATUS =====");

  Serial.print("Weather city: ");
  Serial.println(weatherCity);

  Serial.print("Rain forecast level: ");
  Serial.println(rainForecastLevel);

  Serial.print("Rain forecast: ");
  Serial.println(rainForecastText);

  Serial.print("Max probability of rain: ");
  Serial.print(maxRainProbabilityPercent, 2);
  Serial.println("%");

  Serial.print("Max rain volume (3h): ");
  Serial.print(maxRainVolumeMm, 2);
  Serial.println(" mm");

  Serial.print("Input rain forecast level: ");
  Serial.println(rainForecastLevel);

  Serial.println("Type 1 for rain expected or 0 for no rain");

  Serial.println("=========================");
}

void printRModelStatus(
  const char* rModelMode,
  float modelSoilMoisture,
  float modelPhValue,
  int modelActiveNutrients,
  int modelPotassiumOk,
  int modelRainForecastLevel,
  float irrigationProbability,
  const char* irrigationText
) {
  Serial.println("===== R MODEL STATUS =====");

  Serial.print("R model mode: ");
  Serial.println(rModelMode);

  Serial.print("Model soil moisture: ");
  Serial.println(modelSoilMoisture, 2);

  Serial.print("Model pH value: ");
  Serial.println(modelPhValue, 2);

  Serial.print("Model active nutrients: ");
  Serial.println(modelActiveNutrients);

  Serial.print("Model potassium OK: ");
  Serial.println(modelPotassiumOk);

  Serial.print("Model rain forecast level: ");
  Serial.println(modelRainForecastLevel);

  Serial.print("Irrigation probability: ");
  Serial.print(irrigationProbability * 100.0f, 2);
  Serial.println("%");

  Serial.print("Model decision: ");
  Serial.println(irrigationText);

  Serial.println("Input: Type r1 (irrigate), r0 (do not irrigate), ra (auto)");

  Serial.println("==========================");
}

void printNpkStatus(
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk,
  int activeNutrients
) {
  Serial.println("===== NPK STATUS =====");

  Serial.print("Nitrogen level: ");
  Serial.println(nitrogenLevelOk ? "ADEQUATE" : "INSUFFICIENT");

  Serial.print("Phosphorus level: ");
  Serial.println(phosphorusLevelOk ? "ADEQUATE" : "INSUFFICIENT");

  Serial.print("Potassium level: ");
  Serial.println(potassiumLevelOk ? "ADEQUATE" : "INSUFFICIENT");

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
  int rainForecastLevel,
  int rModelIrrigationDecision,
  float soilMoisture,
  float temperature,
  float phValue,
  bool nitrogenLevelOk,
  bool phosphorusLevelOk,
  bool potassiumLevelOk
) {
  Serial.println("===== IRRIGATION DECISION =====");

  if (rainForecastLevel == 1) {
    Serial.println("Decision: OFF");
    Serial.println("Reason: Rain forecast indicates precipitation");
  } else if (rModelIrrigationDecision == 0) {
    Serial.println("Decision: OFF");
    Serial.println("Reason: R statistical model recommends not irrigating");
  } else if (isnan(soilMoisture) || isnan(temperature)) {
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
    Serial.println("Reason: Local rules and R statistical model both allow irrigation");
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