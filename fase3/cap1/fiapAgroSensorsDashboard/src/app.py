import pandas as pd
import streamlit as st
from pathlib import Path

# ============================
# PAGE CONFIGURATION
# ============================

st.set_page_config(
    page_title="Dashboard Agro Sensors",
    page_icon="📊",
    layout="wide"
)

# ============================
# DATA LOADING
# ============================

DATA_PATH = Path(__file__).resolve().parent.parent / "scripts" / "irrigation_training_data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

# ============================
# PAGE HEADER
# ============================

st.title("📊 Dashboard Agro Sensors")

st.write(
    """
    Dashboard desenvolvido para visualizar dados simulados de irrigação agrícola,
    incluindo umidade do solo, pH, níveis de nutrientes e decisões de irrigação.
    """
)

# ============================
# DATASET VIEW
# ============================

try:
    data = load_data()

    st.success("Base de dados carregada com sucesso.")

    # ============================
    # MAIN METRICS
    # ============================

    average_soil_moisture = data["soil_moisture"].mean()
    average_ph = data["ph_value"].mean()
    total_irrigated_scenarios = data[data["should_irrigate"] == 1].shape[0]
    total_rain_blocked_scenarios = data[
        (data["rain_forecast_level"] == 1) & (data["should_irrigate"] == 0)
    ].shape[0]

    st.subheader("📌 Métricas principais")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Umidade média do solo",
            value=f"{average_soil_moisture:.2f}%"
        )

    with col2:
        st.metric(
            label="pH médio",
            value=f"{average_ph:.2f}"
        )

    with col3:
        st.metric(
            label="Cenários com irrigação",
            value=total_irrigated_scenarios
        )

    with col4:
        st.metric(
            label="Bloqueados por chuva",
            value=total_rain_blocked_scenarios
        )

    st.subheader("📄 Base de dados de irrigação")
    st.dataframe(data, use_container_width=True)

except FileNotFoundError:
    st.error(f"Base de dados não encontrada em: {DATA_PATH}")