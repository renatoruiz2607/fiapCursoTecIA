#include <DHT.h>
#include "pins.h"

#define DHTTYPE DHT22

DHT dht(DHT_PIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  Serial.println("AgroSensorsIntelligence iniciado");
}

void loop() {

  int phRaw = analogRead(PH_SENSOR_PIN);
  int soilRaw = analogRead(SOIL_MOISTURE_PIN);
  int nutrientsRaw = analogRead(NUTRIENTS_PIN);
  int ldrRaw = analogRead(LDR_PIN);

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  Serial.println("=== Sensores ===");

  Serial.print("pH RAW: ");
  Serial.println(phRaw);

  Serial.print("Soil Moisture RAW: ");
  Serial.println(soilRaw);

  Serial.print("Nutrients RAW: ");
  Serial.println(nutrientsRaw);

  Serial.print("Luminosity RAW: ");
  Serial.println(ldrRaw);

  Serial.print("Temperature: ");
  Serial.println(temperature);

  Serial.print("Air Humidity: ");
  Serial.println(humidity);

  Serial.println();

  delay(3000);
}