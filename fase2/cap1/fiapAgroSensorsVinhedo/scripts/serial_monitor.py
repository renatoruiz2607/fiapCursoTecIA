"""
Leitura dos sensores do ESP32 da Fase 2 (Agro Sensors Vinhedo).

Conecta-se à porta serial exposta pelo simulador Wokwi, interpreta o ciclo
de leituras enviado pelo firmware a cada 2 segundos e permite enviar os
comandos de simulação aceitos pelo ESP32 (previsão de chuva e modelo em R).

Uso:
    python scripts/serial_monitor.py           -> menu interativo
    python scripts/serial_monitor.py --once    -> exibe uma leitura e encerra

Pré-requisito: simulador Wokwi em execução com o wokwi.toml desta fase.
"""

import argparse
import os
import sys
import time

try:
    import serial
except ImportError:
    serial = None


# Porta definida em rfc2217ServerPort no wokwi.toml desta fase.
SERIAL_PORT = os.getenv("FASE2_SERIAL_PORT") or "rfc2217://localhost:4001"
BAUD_RATE = 115200

CYCLE_START = "===== AGRO SENSORS VINHEDO ====="
CYCLE_END_KEY = "Water pump"
CYCLE_TIMEOUT_SECONDS = 15

REASON_TRANSLATIONS = {
    "Rain forecast indicates precipitation": "Previsão de chuva indica precipitação",
    "R statistical model recommends not irrigating": "Modelo estatístico em R recomenda não irrigar",
    "DHT22 reading failed": "Falha na leitura do sensor DHT22",
    "Soil moisture is sufficient": "Umidade do solo suficiente",
    "Soil pH is out of ideal range for grapevine": "pH do solo fora da faixa ideal para a videira",
    "Potassium level is not adequate": "Nível de potássio inadequado",
    "Minimum nutrient combination not reached": "Combinação mínima de nutrientes não atingida",
    "Local rules and R statistical model both allow irrigation": (
        "Regras locais e modelo estatístico em R permitem a irrigação"
    ),
}

# Textos enviados pelo firmware (em inglês) e sua exibição em português.
TEXT_TRANSLATIONS = {
    "ADEQUATE": "adequado",
    "INSUFFICIENT": "insuficiente",
    "RAIN EXPECTED": "chuva prevista",
    "NO RAIN": "sem chuva",
    "IRRIGATE": "irrigar",
    "DO NOT IRRIGATE": "não irrigar",
    "AUTO": "automático",
    "MANUAL": "manual",
}


# ============================
# LEITURA
# ============================

def open_connection():
    if serial is None:
        raise RuntimeError("O pacote pyserial não está instalado. Execute: pip install -r requirements.txt")

    connection = serial.serial_for_url(SERIAL_PORT, baudrate=BAUD_RATE, timeout=3)
    connection.reset_input_buffer()

    return connection


def parse_line(line, cycle):
    if ":" not in line:
        return

    key, value = line.split(":", 1)
    cycle[key.strip()] = value.strip()


def read_cycle(connection):
    """
    Lê um ciclo completo enviado pelo firmware, do cabeçalho até o status
    da bomba, e retorna os valores no formato {campo: valor}.
    """
    cycle = None
    deadline = time.time() + CYCLE_TIMEOUT_SECONDS

    while time.time() < deadline:
        line = connection.readline().decode("utf-8", errors="ignore").strip()

        if not line:
            continue

        if line == CYCLE_START:
            cycle = {}
            continue

        if cycle is None:
            continue

        parse_line(line, cycle)

        if line.startswith(CYCLE_END_KEY):
            return cycle

    return None


def send_command(connection, command):
    connection.write(f"{command}\n".encode("utf-8"))
    connection.flush()


# ============================
# EXIBIÇÃO
# ============================

def translate(value):
    return TEXT_TRANSLATIONS.get(value, value)


def print_cycle(cycle):
    reason = cycle.get("Reason", "-")
    decision = cycle.get("Decision", "-")

    print("\n======================================")
    print(" LEITURA DOS SENSORES - FASE 2")
    print("======================================")

    print("\nClima (previsão de chuva):")
    print(f"  Cidade: {cycle.get('Weather city', '-')}")
    print(f"  Previsão: {translate(cycle.get('Rain forecast', '-'))} (nível {cycle.get('Rain forecast level', '-')})")
    print(f"  Probabilidade máxima de chuva: {cycle.get('Max probability of rain', '-')}")
    print(f"  Volume máximo de chuva (3h): {cycle.get('Max rain volume (3h)', '-')}")

    print("\nModelo estatístico (R):")
    print(f"  Modo: {translate(cycle.get('R model mode', '-'))}")
    print(f"  Probabilidade de irrigação: {cycle.get('Irrigation probability', '-')}")
    print(f"  Decisão do modelo: {translate(cycle.get('Model decision', '-'))}")

    print("\nNutrientes (NPK):")
    print(f"  Nitrogênio (N): {translate(cycle.get('Nitrogen level', '-'))}")
    print(f"  Fósforo (P): {translate(cycle.get('Phosphorus level', '-'))}")
    print(f"  Potássio (K): {translate(cycle.get('Potassium level', '-'))}")
    print(f"  Nutrientes ativos: {cycle.get('Active nutrients', '-')}")

    print("\nSolo e ambiente:")
    print(f"  pH do solo: {cycle.get('Simulated soil pH', '-')}")
    print(f"  Umidade do solo: {cycle.get('Simulated soil moisture', '-')}")
    print(f"  Temperatura: {cycle.get('Temperature', '-').replace(' C', ' °C')}")

    print("\nIrrigação:")
    print(f"  Decisão: {'LIGAR' if decision == 'ON' else 'DESLIGAR' if decision == 'OFF' else decision}")
    print(f"  Motivo: {REASON_TRANSLATIONS.get(reason, reason)}")
    print(f"  Bomba d'água: {'LIGADA' if cycle.get('Water pump') == 'ON' else 'DESLIGADA'}")


def read_and_print(connection):
    cycle = read_cycle(connection)

    if not cycle:
        print("\nNenhuma leitura recebida do ESP32. Verifique se o simulador está em execução.")
        return False

    print_cycle(cycle)
    return True


def print_connection_help(error):
    print("\nNão foi possível conectar ao ESP32 da Fase 2.")
    print(f"Detalhe: {error}")

    if "refused" in str(error).lower():
        print("\nO simulador Wokwi não está em execução.")
        print("1. Compile o firmware da Fase 2 (launcher: Fase 2 > Compilar firmware ESP32).")
        print("2. No VS Code, execute 'Wokwi: Select Config File' e escolha o")
        print("   wokwi.toml da pasta fase2/cap1/fiapAgroSensorsVinhedo.")
        print("3. Execute 'Wokwi: Start Simulator' e tente novamente.")


# ============================
# MENU
# ============================

def monitor(connection, total_readings=5):
    print(f"\nMonitorando {total_readings} leituras (uma a cada ~2 segundos). Ctrl+C para interromper.")

    try:
        for _ in range(total_readings):
            if not read_and_print(connection):
                break
    except KeyboardInterrupt:
        print("\nMonitoramento interrompido.")


def send_and_show(connection, command, description):
    send_command(connection, command)
    print(f"\nComando enviado ao ESP32: {command} ({description})")

    # O comando é processado no início do próximo ciclo; descarta o ciclo
    # em andamento e exibe o seguinte, já com o efeito aplicado.
    read_cycle(connection)
    read_and_print(connection)


def show_menu():
    print("\n======================================")
    print(" AGRO SENSORS VINHEDO - SENSORES ESP32")
    print("======================================")
    print("1 - Exibir leitura atual dos sensores")
    print("2 - Monitorar as próximas 5 leituras")
    print("3 - Informar previsão: chuva prevista (1)")
    print("4 - Informar previsão: sem chuva (0)")
    print("5 - Modelo R: forçar irrigar (r1)")
    print("6 - Modelo R: forçar não irrigar (r0)")
    print("7 - Modelo R: voltar ao modo automático (ra)")
    print("0 - Sair")


COMMANDS = {
    "3": ("1", "chuva prevista"),
    "4": ("0", "sem chuva"),
    "5": ("r1", "modelo R força irrigar"),
    "6": ("r0", "modelo R força não irrigar"),
    "7": ("ra", "modelo R em modo automático"),
}


def start_menu(connection):
    while True:
        show_menu()

        try:
            option = input("\nSelecione uma opção: ").strip()
        except (EOFError, KeyboardInterrupt):
            option = "0"

        if option == "0":
            print("\nEncerrando a leitura dos sensores...")
            break

        if option == "1":
            read_and_print(connection)
        elif option == "2":
            monitor(connection)
        elif option in COMMANDS:
            send_and_show(connection, *COMMANDS[option])
        else:
            print("\nOpção inválida.")


def main():
    parser = argparse.ArgumentParser(description="Leitura dos sensores ESP32 - Fase 2")
    parser.add_argument("--once", action="store_true", help="Exibe uma leitura e encerra.")
    arguments = parser.parse_args()

    try:
        connection = open_connection()
    except Exception as error:
        print_connection_help(error)
        return 1

    try:
        if arguments.once:
            return 0 if read_and_print(connection) else 1

        start_menu(connection)
        return 0
    finally:
        connection.close()


if __name__ == "__main__":
    sys.exit(main())
