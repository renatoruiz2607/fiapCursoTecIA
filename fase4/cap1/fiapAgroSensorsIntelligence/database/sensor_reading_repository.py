from database.database import get_connection


def save_sensor_reading(sensor_data):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
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
            recommendation
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
            :recommendation
        )
        """,
        {
            "soil_moisture": sensor_data.get("soil_moisture"),
            "ph": sensor_data.get("ph"),
            "nutrients_level": sensor_data.get("nutrients_level"),
            "luminosity": sensor_data.get("luminosity"),
            "temperature": sensor_data.get("temperature"),
            "air_humidity": sensor_data.get("air_humidity"),
            "productivity_index": sensor_data.get("productivity_index"),
            "productivity_classification": sensor_data.get("productivity_classification"),
            "recommendation": sensor_data.get("recommendation"),
        },
    )

    connection.commit()
    cursor.close()
    connection.close()