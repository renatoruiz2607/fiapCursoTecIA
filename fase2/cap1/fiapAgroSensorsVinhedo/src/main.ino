#include <Arduino.h>
#include <DHT.h>

// =====================================
// FIAP Agro Sensors Vinhedo
// NPK Buttons + LDR + DHT22 + Relay
// =====================================

// ============================
// PIN DEFINITIONS
// ============================

const int NITROGEN_BUTTON_PIN = 14;
const int PHOSPHORUS_BUTTON_PIN = 27;
const int POTASSIUM_BUTTON_PIN = 26;
const int PH_SENSOR_PIN = 34;
const int DHT_SENSOR_PIN = 4;
const int WATER_PUMP_RELAY_PIN = 18;

// ============================
// DHT CONFIGURATION
// ============================

#define DHTTYPE DHT22
DHT dht(DHT_SENSOR_PIN, DHTTYPE);

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
// FUNCTION: Convert LDR to pH
// ============================

float convertLdrToPh(int rawValue) {
  return (rawValue / 4095.0f) * 14.0f;
}

// ============================
// FUNCTION: Read NPK Buttons
// ============================

void readNpkButtons() {
  nitrogenLevelOk = digitalRead(NITROGEN_BUTTON_PIN) == LOW;
  phosphorusLevelOk = digitalRead(PHOSPHORUS_BUTTON_PIN) == LOW;
  potassiumLevelOk = digitalRead(POTASSIUM_BUTTON_PIN) == LOW;
}

// ============================
// FUNCTION: Read pH Sensor
// ============================

void readPhSensor() {
  phRawValue = analogRead(PH_SENSOR_PIN);
  phValue = convertLdrToPh(phRawValue);
}

// ============================
// FUNCTION: Read Soil Moisture Sensor
// ============================

void readSoilMoistureSensor() {
  soilMoisture = dht.readHumidity();
  temperature = dht.readTemperature();
}

// ============================
// FUNCTION: Test Water Pump Relay
// ============================

void testWaterPumpRelay() {
  waterPumpOn = !waterPumpOn;
  digitalWrite(WATER_PUMP_RELAY_PIN, waterPumpOn ? HIGH : LOW);
}

// ============================
// FUNCTION: Print NPK Status
// ============================

void printNpkStatus() {
  Serial.println("===== NPK STATUS =====");

  Serial.print("Nitrogen: ");
  Serial.println(nitrogenLevelOk ? "OK" : "LOW");

  Serial.print("Phosphorus: ");
  Serial.println(phosphorusLevelOk ? "OK" : "LOW");

  Serial.print("Potassium: ");
  Serial.println(potassiumLevelOk ? "OK" : "LOW");

  Serial.println("======================");
}

// ============================
// FUNCTION: Print pH Status
// ============================

void printPhStatus() {
  Serial.println("===== PH SENSOR STATUS =====");

  Serial.print("LDR raw value: ");
  Serial.println(phRawValue);

  Serial.print("Simulated soil pH: ");
  Serial.println(phValue, 2);

  Serial.println("============================");
}

// ============================
// FUNCTION: Print Soil Moisture Status
// ============================

void printSoilMoistureStatus() {
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

// ============================
// FUNCTION: Print Water Pump Status
// ============================

void printWaterPumpStatus() {
  Serial.println("===== WATER PUMP STATUS =====");
  Serial.print("Water pump: ");
  Serial.println(waterPumpOn ? "ON" : "OFF");
  Serial.println("=============================");
  Serial.println();
}

// ============================
// SETUP
// ============================

void setup() {
  Serial.begin(115200);

  pinMode(NITROGEN_BUTTON_PIN, INPUT_PULLUP);
  pinMode(PHOSPHORUS_BUTTON_PIN, INPUT_PULLUP);
  pinMode(POTASSIUM_BUTTON_PIN, INPUT_PULLUP);
  pinMode(PH_SENSOR_PIN, INPUT);
  pinMode(WATER_PUMP_RELAY_PIN, OUTPUT);

  digitalWrite(WATER_PUMP_RELAY_PIN, LOW);

  dht.begin();

  Serial.println("Starting full sensor and relay test...");
  Serial.println();
}

// ============================
// LOOP
// ============================

void loop() {
  readNpkButtons();
  readPhSensor();
  readSoilMoistureSensor();
  testWaterPumpRelay();

  printNpkStatus();
  printPhStatus();
  printSoilMoistureStatus();
  printWaterPumpStatus();

  delay(2000);
}