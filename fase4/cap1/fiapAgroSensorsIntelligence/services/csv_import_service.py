import csv

from database.database import get_connection


CSV_PATH = "data/simulated_sensor_readings.csv"


def import_simulated_csv_to_database():
    rows = []

    try:
        print("\nLendo arquivo CSV...")

        with open(CSV_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                rows.append({
                    "soil_moisture": float(row["soil_moisture"]),
                    "ph": float(row["ph"]),
                    "nutrients_level": float(row["nutrients_level"]),
                    "luminosity": float(row["luminosity"]),
                    "temperature": float(row["temperature"]),
                    "air_humidity": float(row["air_humidity"]),
                    "productivity_index": float(row["productivity_index"]),
                    "productivity_classification": row["productivity_classification"],
                    "recommendation": row["recommendation"],
                    "irrigation_volume": float(row["irrigation_volume"]),
                    "fertilization_need": row["fertilization_need"],
                })

        print(f"Registros encontrados no CSV: {len(rows)}")
        print("Importando registros para o Oracle...")

        connection = get_connection()
        cursor = connection.cursor()

        cursor.executemany(
            """
            INSERT INTO sensor_readings (
                soil_moisture,
                ph,
                nutrients_level,
                luminosity,
                temperature,
                air_humidity,
                productivity_index,
                productivity_classification,
                recommendation,
                irrigation_volume,
                fertilization_need
            )
            VALUES (
                :soil_moisture,
                :ph,
                :nutrients_level,
                :luminosity,
                :temperature,
                :air_humidity,
                :productivity_index,
                :productivity_classification,
                :recommendation,
                :irrigation_volume,
                :fertilization_need
            )
            """,
            rows
        )

        connection.commit()
        cursor.close()
        connection.close()

        print(f"\nImportação concluída. Registros importados: {len(rows)}")

    except FileNotFoundError:
        print(f"\nArquivo não encontrado: {CSV_PATH}")

    except Exception as error:
        print("\nErro ao importar CSV simulado.")
        print(f"Detalhe: {error}")