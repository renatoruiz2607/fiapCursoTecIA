#pragma once

void initializeWeatherInput();

void setRainForecastLevel(int level);

int getRainForecastLevel();

const char* getRainForecastText();

const char* getWeatherCity();

float getMaxRainProbabilityPercent();

float getMaxRainVolumeMm();