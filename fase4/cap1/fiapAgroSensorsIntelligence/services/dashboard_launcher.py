import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
DASHBOARD_PATH = PROJECT_DIR / "dashboard" / "app.py"


def open_dashboard():
    try:
        print("\nIniciando dashboard Streamlit...")

        subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(DASHBOARD_PATH)
            ],
            cwd=PROJECT_DIR
        )

        print("Dashboard iniciado com sucesso.")
        print("Acesse: http://localhost:8501")

    except Exception as error:
        print("\nErro ao iniciar dashboard.")
        print(f"Detalhe: {error}")
