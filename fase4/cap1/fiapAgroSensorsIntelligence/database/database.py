import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATABASE_FILE_NAME = "agro_sensors.db"


def _find_repository_root():
    # A raiz do sistema integrado é identificada pelo launcher.py.
    for parent in Path(__file__).resolve().parents:
        if (parent / "launcher.py").exists():
            return parent

    return None


def get_database_path():
    # Permite sobrescrever o caminho do banco pela variável de ambiente.
    custom_path = os.getenv("AGRO_DB_PATH")

    if custom_path:
        return Path(custom_path).expanduser().resolve()

    # Banco único compartilhado entre as fases, na pasta data da raiz.
    repository_root = _find_repository_root()

    if repository_root:
        return repository_root / "data" / DATABASE_FILE_NAME

    # Execução isolada da Fase 4, fora do sistema integrado.
    return PROJECT_DIR / "data" / DATABASE_FILE_NAME


def get_connection():
    database_path = get_database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(database_path)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

            soil_moisture REAL NOT NULL,
            ph REAL NOT NULL,
            nutrients_level REAL NOT NULL,
            luminosity REAL NOT NULL,
            temperature REAL NOT NULL,
            air_humidity REAL NOT NULL,

            productivity_index REAL NOT NULL,
            productivity_classification TEXT NOT NULL,

            recommendation TEXT NOT NULL,
            irrigation_volume REAL NOT NULL,
            fertilization_need TEXT NOT NULL
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Banco de dados SQLite pronto em: {get_database_path()}")
