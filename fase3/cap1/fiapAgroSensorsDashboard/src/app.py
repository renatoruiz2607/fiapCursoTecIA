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
    Dashboard desenvolvido para visualizar dados de irrigação agrícola,
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
    total_valid_nutrient_scenarios = data[
        (data["active_nutrients"] >= 2) &
        (data["potassium_ok"] == 1)
    ].shape[0]

    st.subheader("📌 Métricas principais")

    col1, col2, col3, col4, col5 = st.columns(5)

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

    with col5:
        st.metric(
            label="Nutrientes adequados",
            value=total_valid_nutrient_scenarios
        )

    # ============================
    # CHARTS
    # ============================

    st.subheader("📈 Gráficos de análise")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("**Distribuição da umidade do solo**")
        st.bar_chart(data["soil_moisture"])

    with col_chart2:
        st.markdown("**Distribuição do pH do solo**")
        st.line_chart(data["ph_value"])

    col_chart3, col_chart4 = st.columns(2)

    col_chart3, col_chart4 = st.columns(2)

    with col_chart3:
        st.markdown("**Umidade média por decisão de irrigação**")

        moisture_by_decision = (
            data.assign(
                irrigation_decision=data["should_irrigate"].map({
                    0: "Não irrigar",
                    1: "Irrigar"
                })
            )
            .groupby("irrigation_decision")["soil_moisture"]
            .mean()
            .sort_values()
        )

        st.bar_chart(moisture_by_decision)

    with col_chart4:
        st.markdown("**Relação entre pH e umidade por decisão de irrigação**")

        scatter_data = data.copy()
        scatter_data["decision_label"] = scatter_data["should_irrigate"].map({
            0: "Não irrigar",
            1: "Irrigar"
        })

        st.scatter_chart(
            scatter_data,
            x="ph_value",
            y="soil_moisture",
            color="decision_label"
        )

    st.subheader("📄 Base de dados de irrigação")
    st.dataframe(data, use_container_width=True)

except FileNotFoundError:
    st.error(f"Base de dados não encontrada em: {DATA_PATH}")