import threading
import time
from datetime import datetime

from serial_sensor_reader import read_current_sensor_data
from database.sensor_reading_repository import save_sensor_reading


_ingestion_thread = None
_stop_event = threading.Event()

_ingestion_status = {
    "active": False,
    "total_saved": 0,
    "last_saved_at": None,
    "last_error": None,
}


def _ingestion_loop(interval_seconds):
    _ingestion_status["active"] = True
    _ingestion_status["last_error"] = None

    while not _stop_event.is_set():
        try:
            sensor_data = read_current_sensor_data()

            if sensor_data:
                save_sensor_reading(sensor_data)

                _ingestion_status["total_saved"] += 1
                _ingestion_status["last_saved_at"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                _ingestion_status["last_error"] = None

        except Exception as error:
            _ingestion_status["last_error"] = str(error)

        _stop_event.wait(interval_seconds)

    _ingestion_status["active"] = False


def start_automatic_ingestion(interval_seconds=10):
    global _ingestion_thread

    if _ingestion_thread and _ingestion_thread.is_alive():
        print("\nA ingestão automática já está ativa.")
        return

    _stop_event.clear()

    _ingestion_thread = threading.Thread(
        target=_ingestion_loop,
        args=(interval_seconds,),
        daemon=True,
    )

    _ingestion_thread.start()

    print(f"\nIngestão automática iniciada. Intervalo: {interval_seconds} segundos.")


def stop_automatic_ingestion():
    if not _ingestion_thread or not _ingestion_thread.is_alive():
        print("\nA ingestão automática não está ativa.")
        return

    _stop_event.set()
    _ingestion_thread.join(timeout=5)

    print("\nIngestão automática parada.")


def show_ingestion_status():
    status = "Ativa" if _ingestion_status["active"] else "Inativa"

    print("\nStatus da ingestão automática:")
    print("--------------------------------------")
    print(f"Status: {status}")
    print(f"Total de registros salvos: {_ingestion_status['total_saved']}")
    print(f"Último registro salvo em: {_ingestion_status['last_saved_at'] or '-'}")
    print(f"Último erro: {_ingestion_status['last_error'] or '-'}")