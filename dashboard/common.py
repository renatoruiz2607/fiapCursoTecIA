"""
Funções compartilhadas pelas páginas da dashboard integrada.
"""

import importlib.util
import os
import sys
from pathlib import Path

import streamlit as st

DASHBOARD_DIR = Path(__file__).resolve().parent
ROOT_DIR = DASHBOARD_DIR.parent
FASE4_DIR = ROOT_DIR / "fase4" / "cap1" / "fiapAgroSensorsIntelligence"
FASE6_DIR = ROOT_DIR / "fase6" / "cap1" / "fiapAgroNeuralNetwork"
ALERTS_DIR = ROOT_DIR / "aws_alerts"

# Raiz (launcher), Fase 4 (banco e ML) e alertas ficam importáveis.
for path in (ROOT_DIR, FASE4_DIR, ALERTS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

try:
    from dotenv import load_dotenv

    load_dotenv(ROOT_DIR / ".env")
except ImportError:
    pass

import launcher  # noqa: E402
from database.database import get_connection, get_database_path  # noqa: E402


# ============================
# STATUS DO SISTEMA
# ============================

def get_database_summary():
    """Retorna o total de leituras e a última leitura registrada."""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM sensor_readings")
        total = cursor.fetchone()[0]
        cursor.close()
        connection.close()
    except Exception:
        return {"total": 0, "latest": None}

    latest = None

    if total:
        from alert_client import get_latest_reading

        latest = get_latest_reading()

    return {"total": total, "latest": latest}


def models_trained():
    return (FASE4_DIR / "ml" / "metrics.json").exists()


def vision_models_status():
    models_dir = FASE6_DIR / "models"

    return {
        "YOLO 60 épocas": (models_dir / "yolo" / "60_epochs" / "best.pt").exists(),
        "YOLO 30 épocas": (models_dir / "yolo" / "30_epochs" / "best.pt").exists(),
        "CNN": (models_dir / "cnn" / "cnn_30_epocas.keras").exists(),
    }


def aws_configured():
    return all(os.getenv(name) for name in launcher.AWS_ENV_VARS)


# ============================
# DASHBOARD DA FASE 4
# ============================

@st.cache_resource
def load_fase4_dashboard():
    """Importa a dashboard da Fase 4 como módulo, sem executá-la."""
    spec = importlib.util.spec_from_file_location(
        "fase4_dashboard",
        FASE4_DIR / "dashboard" / "app.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


# ============================
# PROCESSOS EM SEGUNDO PLANO
# ============================

@st.cache_resource
def get_running_servers():
    """Dashboards das fases iniciadas a partir da página de serviços."""
    return {}
