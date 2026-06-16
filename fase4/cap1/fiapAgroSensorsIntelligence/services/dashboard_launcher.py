import subprocess
import sys


def open_dashboard():
    try:
        print("\nIniciando dashboard Streamlit...")

        subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "dashboard/app.py"
            ]
        )

        print("Dashboard iniciado com sucesso.")
        print("Acesse: http://localhost:8501")

    except Exception as error:
        print("\nErro ao iniciar dashboard.")
        print(f"Detalhe: {error}")