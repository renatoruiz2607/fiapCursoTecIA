#pragma once

void initializeRModelInput();

void setRModelManualDecision(int decision);

void resetRModelToAuto();

float getRModelSoilMoisture();

float getRModelPhValue();

int getRModelActiveNutrients();

int getRModelPotassiumOk();

int getRModelRainForecastLevel();

float getRModelIrrigationProbability();

int getRModelIrrigationDecision();

const char* getRModelIrrigationText();

const char* getRModelMode();