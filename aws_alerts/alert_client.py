"""
Cliente local do serviço de alerta FarmTech.

Envia a leitura dos sensores para a Lambda "farmtech-monitor" na AWS,
que avalia as regras e dispara o e-mail pelo Amazon SNS.

Uso:
    python aws_alerts/alert_client.py --latest     -> última leitura do banco SQLite
    python aws_alerts/alert_client.py --test       -> leitura crítica de teste
    python aws_alerts/alert_client.py --preview    -> mostra o e-mail sem enviar (sem AWS)

Variáveis de ambiente (.env da raiz):
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
    ALERT_LAMBDA_NAME (padrão: farmtech-monitor)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ALERTS_DIR = Path(__file__).resolve().parent
ROOT_DIR = ALERTS_DIR.parent
FASE4_DIR = ROOT_DIR / "fase4" / "cap1" / "fiapAgroSensorsIntelligence"

# Reaproveita a conexão com o banco SQLite da Fase 4.
sys.path.insert(0, str(FASE4_DIR))
sys.path.insert(0, str(ALERTS_DIR))

try:
    from dotenv import load_dotenv

    load_dotenv(ROOT_DIR / ".env")
except ImportError:
    pass

from database.database import get_connection, get_database_path  # noqa: E402
from lambda_function import (  # noqa: E402
    build_message,
    build_subject,
    evaluate_reading,
)


DEFAULT_LAMBDA_NAME = "farmtech-monitor"

BRAZIL_TIMEZONE = timezone(timedelta(hours=-3))

# Leitura com vários problemas, útil para demonstrar o alerta.
TEST_READING = {
    "soil_moisture": 22.0,
    "ph": 4.8,
    "nutrients_level": 35.0,
    "luminosity": 60.0,
    "temperature": 36.5,
    "air_humidity": 30.0,
    "productivity_index": 32.0,
    "irrigation_volume": 0.0,
    "created_at": "leitura de teste (simulada)",
}

READING_COLUMNS = [
    "id",
    "created_at",
    "soil_moisture",
    "ph",
    "nutrients_level",
    "luminosity",
    "temperature",
    "air_humidity",
    "productivity_index",
    "irrigation_volume",
]


def get_latest_reading():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(f"""
            SELECT {", ".join(READING_COLUMNS)}
            FROM sensor_readings
            ORDER BY id DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
    except Exception:
        row = None
    finally:
        cursor.close()
        connection.close()

    if not row:
        return None

    reading = dict(zip(READING_COLUMNS, row))
    reading["created_at"] = format_database_timestamp(reading["created_at"])

    return reading


def format_database_timestamp(value):
    # O SQLite grava CURRENT_TIMESTAMP em UTC; converte para Brasília.
    try:
        utc_time = datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return value

    local_time = utc_time.replace(tzinfo=timezone.utc).astimezone(BRAZIL_TIMEZONE)

    return local_time.strftime("%d/%m/%Y %H:%M:%S") + " (horário de Brasília)"


def invoke_monitor(reading):
    import boto3

    lambda_name = os.getenv("ALERT_LAMBDA_NAME") or DEFAULT_LAMBDA_NAME
    client = boto3.client("lambda")

    response = client.invoke(
        FunctionName=lambda_name,
        InvocationType="RequestResponse",
        Payload=json.dumps({"source": "sensors", "reading": reading}).encode("utf-8"),
    )

    payload = json.loads(response["Payload"].read() or b"{}")

    if response.get("FunctionError"):
        raise RuntimeError(f"Erro na execução da Lambda: {payload}")

    return payload


def print_reading(reading):
    print("Leitura analisada:")
    print("--------------------------------------")
    print(f"Registro: {reading.get('id', '-')} | {reading.get('created_at', '-')}")
    print(f"Umidade do solo: {reading['soil_moisture']:.1f}%")
    print(f"pH: {reading['ph']:.1f}")
    print(f"Nutrientes: {reading['nutrients_level']:.1f}%")
    print(f"Temperatura: {reading['temperature']:.1f} °C")
    print(f"Umidade do ar: {reading['air_humidity']:.1f}%")
    print(f"Produtividade: {reading['productivity_index']:.1f}/100")


def show_preview(reading):
    alerts = evaluate_reading(reading)

    if not alerts:
        print("\nNenhum alerta para esta leitura. Nenhum e-mail seria enviado.")
        return

    print("\nPrévia do e-mail (não enviado):")
    print("======================================")
    print(f"Assunto: {build_subject(alerts)}\n")
    print(build_message(reading, alerts))


def send_alert(reading):
    print("\nEnviando leitura ao serviço de monitoramento na AWS...")

    result = invoke_monitor(reading)

    if result.get("status") == "error":
        print(f"A Lambda recusou a leitura: {result.get('error')}")
        return 1

    if not result.get("alert_sent"):
        print(result.get("message", "Nenhum alerta enviado."))
        return 0

    print("\nAlerta enviado por e-mail com sucesso.")
    print(f"Assunto: {result['subject']}")
    print(f"ID da mensagem (SNS): {result['message_id']}")
    print("\nAlertas:")

    for alert in result["alerts"]:
        print(f"- [{alert['severity']}] {alert['problem']}")

    return 0


def parse_arguments():
    parser = argparse.ArgumentParser(description="Serviço de alerta FarmTech (AWS)")
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--latest", action="store_true", help="Envia a última leitura do banco (padrão).")
    group.add_argument("--test", action="store_true", help="Envia uma leitura crítica de teste.")

    parser.add_argument("--preview", action="store_true", help="Mostra o e-mail sem enviar.")

    return parser.parse_args()


def main():
    arguments = parse_arguments()

    if arguments.test:
        reading = TEST_READING
    else:
        reading = get_latest_reading()

        if not reading:
            print("Nenhuma leitura encontrada no banco de dados.")
            print(f"Banco: {get_database_path()}")
            print("Importe o CSV ou salve uma leitura pela Fase 4 antes de enviar o alerta.")
            return 1

    print_reading(reading)

    if arguments.preview:
        show_preview(reading)
        return 0

    try:
        return send_alert(reading)

    except ModuleNotFoundError:
        print("\nO pacote boto3 não está instalado. Execute: pip install -r requirements.txt")
        return 1

    except Exception as error:
        print("\nNão foi possível enviar o alerta.")
        print(f"Detalhe: {error}")
        print("Verifique as credenciais AWS e o nome da Lambda no arquivo .env.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
