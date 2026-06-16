import pandas as pd

from database.database import get_connection


NUMERIC_COLUMNS = [
    "soil_moisture",
    "ph",
    "nutrients_level",
    "luminosity",
    "temperature",
    "air_humidity",
    "productivity_index",
    "irrigation_volume",
]


def load_sensor_dataset():
    connection = get_connection()

    query = """
        SELECT
            soil_moisture,
            ph,
            nutrients_level,
            luminosity,
            temperature,
            air_humidity,
            productivity_index,
            irrigation_volume,
            fertilization_need
        FROM sensor_readings
        ORDER BY created_at
    """

    dataframe = pd.read_sql(query, connection)
    connection.close()

    dataframe.columns = [column.lower() for column in dataframe.columns]

    for column in NUMERIC_COLUMNS:
        dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")

    dataframe = dataframe.dropna(subset=NUMERIC_COLUMNS)

    return dataframe


def validate_dataset(dataframe, minimum_rows=50):
    if dataframe.empty:
        raise ValueError("O dataset está vazio. Importe o CSV simulado ou salve leituras no banco.")

    if len(dataframe) < minimum_rows:
        raise ValueError(
            f"O dataset possui apenas {len(dataframe)} registros. "
            f"Para treinar os modelos, recomenda-se pelo menos {minimum_rows} registros."
        )