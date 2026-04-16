#include <Arduino.h>

#include "r_model_input.h"
#include "generated_irrigation_model_data.h"

// ============================
// INTERNAL STATE
// ============================

static int currentRModelIrrigationDecision = DEFAULT_R_MODEL_IRRIGATION_DECISION;
static bool isRModelManualOverrideEnabled = false;

// ============================
// INITIALIZATION
// ============================

void initializeRModelInput() {
  currentRModelIrrigationDecision = DEFAULT_R_MODEL_IRRIGATION_DECISION;
  isRModelManualOverrideEnabled = false;
}

// ============================
// SERIAL INPUT HANDLER
// ============================

void setRModelManualDecision(int decision) {
  currentRModelIrrigationDecision = decision;
  isRModelManualOverrideEnabled = true;
}

void resetRModelToAuto() {
  currentRModelIrrigationDecision = DEFAULT_R_MODEL_IRRIGATION_DECISION;
  isRModelManualOverrideEnabled = false;
}

// ============================
// GETTERS
// ============================

float getRModelSoilMoisture() {
  return DEFAULT_R_MODEL_SOIL_MOISTURE;
}

float getRModelPhValue() {
  return DEFAULT_R_MODEL_PH_VALUE;
}

int getRModelActiveNutrients() {
  return DEFAULT_R_MODEL_ACTIVE_NUTRIENTS;
}

int getRModelPotassiumOk() {
  return DEFAULT_R_MODEL_POTASSIUM_OK;
}

int getRModelRainForecastLevel() {
  return DEFAULT_R_MODEL_RAIN_FORECAST_LEVEL;
}

float getRModelIrrigationProbability() {
  return DEFAULT_R_MODEL_IRRIGATION_PROBABILITY;
}

int getRModelIrrigationDecision() {
  return currentRModelIrrigationDecision;
}

const char* getRModelIrrigationText() {
  if (currentRModelIrrigationDecision == 1) {
    return "IRRIGATE";
  }

  return "DO NOT IRRIGATE";
}

const char* getRModelMode() {
  if (isRModelManualOverrideEnabled) {
    return "MANUAL";
  }

  return "AUTO";
}