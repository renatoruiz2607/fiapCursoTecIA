#include <Arduino.h>

#include "weather_input.h"

// ============================
// GLOBAL VARIABLE
// ============================

static int rainForecastLevel = 0;

// ============================
// INITIALIZATION
// ============================

void initializeWeatherInput() {
  rainForecastLevel = 0;
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

    // clean buffer (remove \n or \r)
    while (Serial.available()) {
      Serial.read();
    }
  }
}

// ============================
// GETTER
// ============================

int getRainForecastLevel() {
  return rainForecastLevel;
}