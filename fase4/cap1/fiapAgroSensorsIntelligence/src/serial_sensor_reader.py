import serial
import time


SERIAL_PORT = "rfc2217://localhost:4000"
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
        return None