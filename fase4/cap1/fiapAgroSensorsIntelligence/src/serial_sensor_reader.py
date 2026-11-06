import os
import time

import serial


# Porta padrão exposta pelo simulador Wokwi (rfc2217ServerPort no wokwi.toml).
# Pode ser alterada pela variável SENSOR_SERIAL_PORT para usar um ESP32 físico.
SERIAL_PORT = os.getenv("SENSOR_SERIAL_PORT") or "rfc2217://localhost:4000"
BAUD_RATE = 115200


def parse_sensor_line(line):
    sensor_data = {}

    parts = line.split(";")

    for part in parts:
        if "=" not in part:
            continue

        key, value = part.split("=", 1)

        key = key.strip()
        value = value.strip()

        try:
            sensor_data[key] = float(value)
        except ValueError:
            sensor_data[key] = value

    return sensor_data


def read_current_sensor_data():
    try:
        with serial.serial_for_url(SERIAL_PORT, baudrate=BAUD_RATE, timeout=10) as ser:
            time.sleep(2)

            while True:
                line = ser.readline().decode("utf-8", errors="ignore").strip()

                if not line:
                    continue

                if "soil_moisture=" in line:
                    return parse_sensor_line(line)

    except Exception as error:
        print("\nNão foi possível ler os sensores pela serial.")
        print(f"Detalhe: {error}")

        if "Connection refused" in str(error):
            print("\nO simulador Wokwi não está em execução.")
            print("1. Compile o firmware da Fase 4 (launcher: Fase 4 > Compilar firmware ESP32).")
            print("2. No VS Code, execute 'Wokwi: Select Config File' e escolha o")
            print("   wokwi.toml da pasta fase4/cap1/fiapAgroSensorsIntelligence.")
            print("3. Execute 'Wokwi: Start Simulator' e tente novamente.")

        return None