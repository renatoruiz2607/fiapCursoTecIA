import argparse
import csv
from pathlib import Path

from database.database import get_connection, initialize_database


PROJECT_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_DIR / "data" / "simulated_sensor_readings.csv"

# Campos usados para identificar se uma linha do CSV já está no banco.
IDENTITY_COLUMNS = [
    "soil_moisture",
    "ph",
    "nutrients_level",
    "luminosity",
    "temperature",
    "air_humidity",
    "productivity_index",
    "irrigation_volume",
]


def read_csv_rows():
    rows = []

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

    return rows


def row_exists(cursor, row):
    conditions = " AND ".join(f"{column} = :{column}" for column in IDENTITY_COLUMNS)

    cursor.execute(
        f"SELECT 1 FROM sensor_readings WHERE {conditions} LIMIT 1",
        {column: row[column] for column in IDENTITY_COLUMNS},
    )

    return cursor.fetchone() is not None


def is_csv_already_imported(cursor, rows):
    # O CSV é considerado importado quando a primeira e a última
    # linha já existem no banco, evitando registros duplicados.
    return row_exists(cursor, rows[0]) and row_exists(cursor, rows[-1])


def count_readings(cursor):
    cursor.execute("SELECT COUNT(*) FROM sensor_readings")
    return cursor.fetchone()[0]


def insert_rows(cursor, rows):
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


def import_simulated_csv_to_database():
    try:
        print("\nLendo arquivo CSV...")
        rows = read_csv_rows()
        print(f"Registros encontrados no CSV: {len(rows)}")

        if not rows:
            print("\nO arquivo CSV está vazio. Nada foi importado.")
            return

        initialize_database()
        connection = get_connection()
        cursor = connection.cursor()

        if is_csv_already_imported(cursor, rows):
            print("\nO CSV simulado já foi importado anteriormente.")
            print(f"Registros atuais no banco: {count_readings(cursor)}")
            print("Nenhum registro foi duplicado.")
            print("Para recomeçar do zero, use a opção 'Limpar banco e reimportar CSV'.")

            cursor.close()
            connection.close()
            return

        print("Importando registros para o banco de dados SQLite...")

        insert_rows(cursor, rows)
        connection.commit()

        print(f"\nImportação concluída. Registros importados: {len(rows)}")
        print(f"Registros atuais no banco: {count_readings(cursor)}")

        cursor.close()
        connection.close()

    except FileNotFoundError:
        print(f"\nArquivo não encontrado: {CSV_PATH}")

    except Exception as error:
        print("\nErro ao importar CSV simulado.")
        print(f"Detalhe: {error}")


def reset_database_and_import(confirm=True):
    """
    Remove todas as leituras do banco (inclusive as salvas pelos sensores),
    reinicia a numeração dos registros e importa o CSV simulado novamente.
    """
    try:
        initialize_database()
        connection = get_connection()
        cursor = connection.cursor()
        total = count_readings(cursor)

        if confirm:
            print(f"\nO banco possui {total} registros, incluindo leituras salvas pelos sensores.")
            answer = input("Todos serão apagados. Deseja continuar? (s/n): ").strip().lower()

            if answer not in ("s", "sim"):
                print("\nOperação cancelada. Nenhum registro foi apagado.")
                cursor.close()
                connection.close()
                return

        cursor.execute("DELETE FROM sensor_readings")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'sensor_readings'")
        connection.commit()

        cursor.close()
        connection.close()

        print(f"\nBanco limpo. Registros removidos: {total}")

    except Exception as error:
        print("\nErro ao limpar o banco de dados.")
        print(f"Detalhe: {error}")
        return

    import_simulated_csv_to_database()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Importação do CSV simulado - Fase 4")

    parser.add_argument(
        "--reset",
        action="store_true",
        help="Limpa todas as leituras do banco antes de importar o CSV.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirma a limpeza sem perguntar (uso pela dashboard).",
    )

    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()

    if arguments.reset:
        reset_database_and_import(confirm=not arguments.yes)
    else:
        import_simulated_csv_to_database()
