"""
Launcher do sistema integrado FarmTech.

Ponto único para disparar os serviços desenvolvidos nas fases anteriores,
seja pelo terminal ou pela dashboard (que reutiliza as funções deste módulo).

Uso no terminal:
    python launcher.py                    -> abre o menu interativo por fase
    python launcher.py dashboard          -> abre a dashboard integrada
    python launcher.py list               -> lista os serviços disponíveis
    python launcher.py run <servico>      -> executa um serviço
    python launcher.py <servico>          -> atalho para "run"

Argumentos extras são repassados ao serviço, por exemplo:
    python launcher.py run fase6-yolo-60 --source minha_imagem.jpg
"""

import importlib.util
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # python-dotenv é opcional para o launcher
    load_dotenv = None


ROOT_DIR = Path(__file__).resolve().parent

FASE1_DIR = ROOT_DIR / "fase1" / "fiapAgroInsightVinhedo"
FASE2_DIR = ROOT_DIR / "fase2" / "cap1" / "fiapAgroSensorsVinhedo"
FASE3_DIR = ROOT_DIR / "fase3" / "cap1" / "fiapAgroSensorsDashboard"
FASE4_DIR = ROOT_DIR / "fase4" / "cap1" / "fiapAgroSensorsIntelligence"
FASE6_DIR = ROOT_DIR / "fase6" / "cap1" / "fiapAgroNeuralNetwork"
ALERTS_DIR = ROOT_DIR / "aws_alerts"

AWS_ENV_VARS = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"]

PYTHON = sys.executable

# Nome de cada projeto, exibido no menu interativo.
PHASES = {
    "Fase 1": "Agro Insight Vinhedo",
    "Fase 2": "Agro Sensors Vinhedo",
    "Fase 3": "Agro Sensors Dashboard",
    "Fase 4": "Agro Sensors Intelligence",
    "Fase 6": "Agro Neural Network",
    "Alertas AWS": "FarmTech Monitor",
    "Dashboard": "Sistema Integrado",
}

# Tipos de execução:
# - task: executa e termina, a saída pode ser exibida na dashboard
# - interactive: exige interação no terminal (menus com input)
# - server: processo contínuo (ex.: Streamlit), iniciado em segundo plano
KIND_TASK = "task"
KIND_INTERACTIVE = "interactive"
KIND_SERVER = "server"


@dataclass
class Service:
    key: str
    phase: str
    name: str
    description: str
    command: list
    cwd: Path
    kind: str = KIND_TASK
    requires: list = field(default_factory=list)
    env_vars: list = field(default_factory=list)
    modules: list = field(default_factory=list)
    url: str = None
    # Confirmação exigida na dashboard e argumentos que a dispensam no script.
    confirm: str = None
    confirm_args: list = field(default_factory=list)


SERVICES = [
    # ============================
    # FASE 1 - AGRO INSIGHT VINHEDO
    # ============================
    Service(
        key="fase1-menu",
        phase="Fase 1",
        name="Menu de culturas e insumos",
        description="Cadastro de culturas, cálculo de área/insumos e exportação para CSV.",
        command=[PYTHON, "src/main.py"],
        cwd=FASE1_DIR,
        kind=KIND_INTERACTIVE,
    ),
    Service(
        key="fase1-estatisticas",
        phase="Fase 1",
        name="Estatísticas agrícolas (R)",
        description="Análise estatística dos dados agrícolas exportados.",
        command=["Rscript", "scripts/agricultural_statistics.R"],
        cwd=FASE1_DIR,
        requires=["Rscript"],
    ),
    Service(
        key="fase1-clima",
        phase="Fase 1",
        name="Relatório meteorológico (R)",
        description="Relatório do clima para apoio ao manejo do vinhedo.",
        command=["Rscript", "scripts/weather_report.R"],
        cwd=FASE1_DIR,
        requires=["Rscript"],
    ),

    # ============================
    # FASE 2 - SENSORES IOT (ESP32)
    # ============================
    Service(
        key="fase2-previsao-chuva",
        phase="Fase 2",
        name="Previsão de chuva (OpenWeather)",
        description="Consulta a previsão de 24h e define o nível de chuva usado pelo ESP32.",
        command=[PYTHON, "scripts/weather_api.py"],
        cwd=FASE2_DIR,
        env_vars=["OPENWEATHER_API_KEY"],
    ),
    Service(
        key="fase2-firmware",
        phase="Fase 2",
        name="Compilar firmware ESP32",
        description="Gera os headers (clima e modelo R) e compila o firmware para o Wokwi.",
        command=["pio", "run"],
        cwd=FASE2_DIR,
        requires=["pio", "Rscript"],
        env_vars=["OPENWEATHER_API_KEY"],
    ),

    # ============================
    # FASE 3 - BANCO DE DADOS
    # ============================
    Service(
        key="fase3-dashboard",
        phase="Fase 3",
        name="Dashboard de irrigação",
        description="Visualização dos dados de irrigação e sensores.",
        command=[PYTHON, "-m", "streamlit", "run", "src/app.py", "--server.port", "8503"],
        cwd=FASE3_DIR,
        kind=KIND_SERVER,
        url="http://localhost:8503",
    ),

    # ============================
    # FASE 4 - ML E DASHBOARD
    # ============================
    Service(
        key="fase4-iniciar-banco",
        phase="Fase 4",
        name="Inicializar banco SQLite",
        description="Cria a tabela de leituras dos sensores no banco compartilhado.",
        command=[PYTHON, "-m", "database.database"],
        cwd=FASE4_DIR,
    ),
    Service(
        key="fase4-importar-csv",
        phase="Fase 4",
        name="Importar leituras simuladas",
        description="Popula o banco com o histórico simulado (não duplica se já importado).",
        command=[PYTHON, "-m", "services.csv_import_service"],
        cwd=FASE4_DIR,
    ),
    Service(
        key="fase4-reimportar-csv",
        phase="Fase 4",
        name="Limpar banco e reimportar CSV",
        description="Apaga todas as leituras e importa o CSV simulado do zero (pede confirmação).",
        command=[PYTHON, "-m", "services.csv_import_service", "--reset"],
        cwd=FASE4_DIR,
        confirm="Todas as leituras do banco, inclusive as salvas pelos sensores, serão apagadas.",
        confirm_args=["--yes"],
    ),
    Service(
        key="fase4-treinar",
        phase="Fase 4",
        name="Treinar modelos de ML",
        description="Treina os modelos de regressão e salva as métricas.",
        command=[PYTHON, "-m", "ml.train_models"],
        cwd=FASE4_DIR,
    ),
    Service(
        key="fase4-prever",
        phase="Fase 4",
        name="Executar previsão agrícola",
        description="Gera previsões e recomendações a partir da última leitura.",
        command=[PYTHON, "-m", "ml.prediction_service"],
        cwd=FASE4_DIR,
    ),
    Service(
        key="fase4-firmware",
        phase="Fase 4",
        name="Compilar firmware ESP32",
        description="Compila o firmware dos sensores para a simulação no Wokwi.",
        command=["pio", "run"],
        cwd=FASE4_DIR,
        requires=["pio"],
    ),
    Service(
        key="fase4-menu",
        phase="Fase 4",
        name="Menu dos sensores (ESP32/Wokwi)",
        description="Leitura serial do ESP32 (requer o simulador Wokwi em execução).",
        command=[PYTHON, "src/main.py"],
        cwd=FASE4_DIR,
        kind=KIND_INTERACTIVE,
    ),
    Service(
        key="fase4-dashboard",
        phase="Fase 4",
        name="Dashboard preditiva",
        description="Dashboard analítica original da Fase 4.",
        command=[PYTHON, "-m", "streamlit", "run", "dashboard/app.py", "--server.port", "8502"],
        cwd=FASE4_DIR,
        kind=KIND_SERVER,
        url="http://localhost:8502",
    ),

    # ============================
    # FASE 6 - VISÃO COMPUTACIONAL
    # ============================
    Service(
        key="fase6-yolo-60",
        phase="Fase 6",
        name="YOLOv5 adaptado (60 épocas)",
        description="Detecta controle PS5 e garrafa térmica nas imagens de teste.",
        command=[PYTHON, "src/vision_service.py", "--model", "yolo-60"],
        cwd=FASE6_DIR,
        modules=["torch"],
    ),
    Service(
        key="fase6-yolo-30",
        phase="Fase 6",
        name="YOLOv5 adaptado (30 épocas)",
        description="Mesma detecção com o modelo treinado por 30 épocas.",
        command=[PYTHON, "src/vision_service.py", "--model", "yolo-30"],
        cwd=FASE6_DIR,
        modules=["torch"],
    ),
    Service(
        key="fase6-yolo-coco",
        phase="Fase 6",
        name="YOLOv5 padrão (COCO)",
        description="Detecção de objetos genéricos com os pesos originais, sem fine-tuning.",
        command=[PYTHON, "src/vision_service.py", "--model", "yolo-coco"],
        cwd=FASE6_DIR,
        modules=["torch"],
    ),
    Service(
        key="fase6-cnn",
        phase="Fase 6",
        name="CNN construída do zero",
        description="Classifica cada imagem como controle PS5 ou garrafa térmica.",
        command=[PYTHON, "src/vision_service.py", "--model", "cnn"],
        cwd=FASE6_DIR,
        modules=["tensorflow"],
    ),

    # ============================
    # ALERTAS - MENSAGERIA AWS
    # ============================
    Service(
        key="alertas-ultima-leitura",
        phase="Alertas AWS",
        name="Enviar alerta da última leitura",
        description="Envia a última leitura do banco à Lambda, que avalia e dispara o e-mail (SNS).",
        command=[PYTHON, "aws_alerts/alert_client.py", "--latest"],
        cwd=ROOT_DIR,
        modules=["boto3"],
        env_vars=AWS_ENV_VARS,
    ),
    Service(
        key="alertas-teste",
        phase="Alertas AWS",
        name="Enviar alerta de teste (leitura crítica)",
        description="Envia uma leitura simulada com vários problemas para validar o serviço.",
        command=[PYTHON, "aws_alerts/alert_client.py", "--test"],
        cwd=ROOT_DIR,
        modules=["boto3"],
        env_vars=AWS_ENV_VARS,
    ),
    Service(
        key="alertas-previa",
        phase="Alertas AWS",
        name="Prévia do alerta da última leitura",
        description="Mostra os alertas e o e-mail que seriam enviados, sem acessar a AWS.",
        command=[PYTHON, "aws_alerts/alert_client.py", "--latest", "--preview"],
        cwd=ROOT_DIR,
    ),

    # ============================
    # DASHBOARD INTEGRADA
    # ============================
    Service(
        key="dashboard",
        phase="Dashboard",
        name="Dashboard integrada",
        description="Painel único com sensores, previsões, serviços, visão computacional e alertas.",
        command=[PYTHON, "-m", "streamlit", "run", "dashboard/app.py", "--server.port", "8501"],
        cwd=ROOT_DIR,
        kind=KIND_SERVER,
        url="http://localhost:8501",
    ),
]

SERVICES_BY_KEY = {service.key: service for service in SERVICES}

# Locais conhecidos de programas que podem não estar no PATH.
# O PlatformIO instalado pela extensão do VS Code fica em ~/.platformio/penv.
KNOWN_PROGRAM_PATHS = {
    "pio": [
        Path.home() / ".platformio" / "penv" / "bin" / "pio",
        Path.home() / ".platformio" / "penv" / "Scripts" / "pio.exe",
    ],
}


def load_environment():
    # Carrega o .env da raiz para repassar as variáveis aos serviços.
    if load_dotenv:
        load_dotenv(ROOT_DIR / ".env")


def get_service(key):
    service = SERVICES_BY_KEY.get(key)

    if not service:
        raise KeyError(f"Serviço não encontrado: {key}")

    return service


def resolve_program(program):
    # Procura o programa no PATH e, se não encontrar, nos locais conhecidos.
    found = shutil.which(program)

    if found:
        return found

    for candidate in KNOWN_PROGRAM_PATHS.get(program, []):
        if candidate.exists():
            return str(candidate)

    return None


def check_requirements(service):
    # Retorna a lista de pendências (programas ou variáveis ausentes).
    problems = []

    for program in service.requires:
        if resolve_program(program) is None:
            problems.append(f"Programa '{program}' não encontrado no PATH.")

    for module in service.modules:
        if importlib.util.find_spec(module) is None:
            requirements_file = (
                "requirements-vision.txt"
                if module in ("torch", "tensorflow")
                else "requirements.txt"
            )
            problems.append(
                f"Pacote Python '{module}' não instalado. "
                f"Execute: pip install -r {requirements_file}"
            )

    for variable in service.env_vars:
        if not os.getenv(variable):
            problems.append(
                f"Variável de ambiente '{variable}' não definida. "
                "Copie o .env.example da raiz para .env e preencha o valor."
            )

    if not service.cwd.exists():
        problems.append(f"Pasta do serviço não encontrada: {service.cwd}")

    return problems


def run_service(key, capture_output=False, extra_args=None):
    """
    Executa um serviço.

    - task / interactive: aguarda o término e retorna o CompletedProcess.
      Com capture_output=True, a saída fica disponível para a dashboard.
    - server: inicia em segundo plano e retorna o Popen.
    """
    load_environment()
    service = get_service(key)

    problems = check_requirements(service)

    if problems:
        raise RuntimeError("\n".join(problems))

    # Ignora variáveis vazias do .env (ex.: SSL_CERT_FILE= sem valor),
    # para não sobrescrever o comportamento padrão dos programas.
    environment = {
        name: value for name, value in os.environ.items() if value != ""
    }
    environment["PYTHONIOENCODING"] = "utf-8"

    # Usa o caminho completo do programa quando ele não está no PATH.
    command = list(service.command) + list(extra_args or [])

    if command[0] in service.requires:
        command[0] = resolve_program(command[0])

    if service.kind == KIND_SERVER:
        return subprocess.Popen(command, cwd=service.cwd, env=environment)

    return subprocess.run(
        command,
        cwd=service.cwd,
        env=environment,
        capture_output=capture_output,
        # Sem terminal (ex.: dashboard), nenhuma entrada é aguardada.
        stdin=subprocess.DEVNULL if capture_output else None,
        text=True,
    )


def print_services():
    print("\nServiços disponíveis no sistema integrado:\n")

    current_phase = None

    for service in SERVICES:
        if service.phase != current_phase:
            current_phase = service.phase
            print(f"[{current_phase}]")

        kind_label = {
            KIND_TASK: "",
            KIND_INTERACTIVE: " (interativo)",
            KIND_SERVER: " (servidor)",
        }[service.kind]

        print(f"  {service.key:<24} {service.name}{kind_label}")

    print("\nUso: python launcher.py run <servico>")


# ============================
# MENU INTERATIVO
# ============================

_running_servers = {}


def _ask_option(message):
    try:
        return input(message).strip()
    except (EOFError, KeyboardInterrupt):
        return "0"


def _pause():
    _ask_option("\nPressione ENTER para continuar...")


def _start_server_from_menu(service):
    process = _running_servers.get(service.key)

    if process and process.poll() is None:
        print(f"\nO serviço já está em execução em: {service.url}")
        return

    _running_servers[service.key] = run_service(service.key)

    print(f"\nServiço iniciado em segundo plano: {service.url}")
    print("Ele será encerrado ao sair do menu principal.")


def _execute_from_menu(service):
    print(f"\n>>> {service.phase} | {service.name}\n", flush=True)

    try:
        if service.kind == KIND_SERVER:
            _start_server_from_menu(service)
            return

        result = run_service(service.key)

        if result.returncode != 0:
            print(f"\nO serviço terminou com código {result.returncode}.")

    except RuntimeError as error:
        print("Não foi possível executar o serviço:")
        print(error)

    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")


def _stop_running_servers():
    for key, process in _running_servers.items():
        if process.poll() is None:
            print(f"Encerrando {get_service(key).name}...")
            process.terminate()

    _running_servers.clear()


def _show_phase_menu(phase):
    services = [service for service in SERVICES if service.phase == phase]

    while True:
        print("\n======================================")
        print(f" {phase.upper()} - {PHASES[phase].upper()}")
        print("======================================")

        for index, service in enumerate(services, start=1):
            kind_label = {
                KIND_TASK: "",
                KIND_INTERACTIVE: " [interativo]",
                KIND_SERVER: " [abre no navegador]",
            }[service.kind]

            print(f"{index} - {service.name}{kind_label}")
            print(f"    {service.description}")

        print("0 - Voltar")

        option = _ask_option("\nSelecione um serviço: ")

        if option == "0":
            return

        if option.isdigit() and 1 <= int(option) <= len(services):
            _execute_from_menu(services[int(option) - 1])
            _pause()
        else:
            print("\nOpção inválida.")


def interactive_menu():
    phases = list(PHASES)

    try:
        while True:
            print("\n======================================")
            print(" FARMTECH - SISTEMA INTEGRADO")
            print("======================================")

            for index, phase in enumerate(phases, start=1):
                print(f"{index} - {phase} ({PHASES[phase]})")

            print("0 - Sair")

            option = _ask_option("\nSelecione uma fase: ")

            if option == "0":
                print("\nEncerrando o sistema...")
                break

            if option.isdigit() and 1 <= int(option) <= len(phases):
                _show_phase_menu(phases[int(option) - 1])
            else:
                print("\nOpção inválida.")

    finally:
        _stop_running_servers()


def main(arguments):
    if not arguments:
        interactive_menu()
        return 0

    if arguments[0] in ("list", "-h", "--help", "help"):
        print(__doc__)
        print_services()
        return 0

    if arguments[0] == "run":
        if len(arguments) < 2:
            print("Informe o serviço. Ex.: python launcher.py run fase4-treinar")
            return 1
        key = arguments[1]
        extra_args = arguments[2:]
    else:
        key = arguments[0]
        extra_args = arguments[1:]

    # Caminhos relativos informados pelo usuário são convertidos para
    # absolutos, pois cada serviço roda a partir da pasta da sua fase.
    extra_args = [
        str(Path(argument).resolve()) if Path(argument).exists() else argument
        for argument in extra_args
    ]

    try:
        service = get_service(key)
        print(f"\n>>> {service.phase} | {service.name}\n", flush=True)

        result = run_service(key, extra_args=extra_args)

        if service.kind == KIND_SERVER:
            print(f"Serviço iniciado em: {service.url}")
            print("Pressione Ctrl+C para encerrar.")
            try:
                result.wait()
            except KeyboardInterrupt:
                result.terminate()
            return 0

        return result.returncode

    except KeyError as error:
        print(error.args[0])
        print_services()
        return 1

    except RuntimeError as error:
        print("Não foi possível executar o serviço:")
        print(error)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
