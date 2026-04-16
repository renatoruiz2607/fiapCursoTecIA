#pragma once

void initializeWeatherInput();

void updateRainForecastFromSerial();

int getRainForecastLevel();

const char* getRainForecastText();

const char* getWeatherCity();

float getMaxRainProbabilityPercent();

float getMaxRainVolumeMm();