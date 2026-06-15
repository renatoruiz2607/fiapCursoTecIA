from serial_sensor_reader import read_current_sensor_data


def show_current_sensor_data():
    sensor_data = read_current_sensor_data()

    if not sensor_data:
        print("\nNenhuma leitura válida foi encontrada.")
        return

    print("\nLeitura atual dos sensores:")
    print("--------------------------------------")
    print(f"Umidade do solo: {sensor_data.get('soil_moisture', 0):.1f}%")
    print(f"pH do solo: {sensor_data.get('ph', 0):.1f}")
    print(f"Nível de nutrientes: {sensor_data.get('nutrients_level', 0):.1f}%")
    print(f"Luminosidade: {sensor_data.get('luminosity', 0):.1f}%")
    print(f"Temperatura: {sensor_data.get('temperature', 0):.1f} °C")
    print(f"Umidade do ar: {sensor_data.get('air_humidity', 0):.1f}%")