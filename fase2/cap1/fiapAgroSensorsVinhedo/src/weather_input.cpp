#include <Arduino.h>

#include "weather_input.h"
#include "generated_weather_data.h"

// ============================
// INTERNAL STATE
// ============================

static int rainForecastLevel = DEFAULT_RAIN_FORECAST_LEVEL;

// ============================
// INITIALIZATION
// ============================

void initializeWeatherInput() {
  rainForecastLevel = DEFAULT_RAIN_FORECAST_LEVEL;
}

// ============================
// SERIAL INPUT HANDLER
// ============================

void updateRainForecastFromSerial() {
  if (Serial.available() > 0) {
    char input = Serial.read();

    if (input == '0') {
      rainForecastLevel = 0;
    } 
    else if (input == '1') {
      rainForecastLevel = 1;
    }

    while (Serial.available()) {
      Serial.read();
    }
  }
}

// ============================
// GETTERS
// ============================

int getRainForecastLevel() {
  return rainForecastLevel;
}

const char* getRainForecastText() {
  if (rainForecastLevel == 1) {
    return "RAIN EXPECTED";
  }

  return "NO RAIN";
}

const char* getWeatherCity() {
  return DEFAULT_WEATHER_CITY;
}

float getMaxRainProbabilityPercent() {
  return DEFAULT_MAX_RAIN_PROBABILITY_PERCENT;
}

float getMaxRainVolumeMm() {
  return DEFAULT_MAX_RAIN_VOLUME_MM;
}