import streamlit as st

import common

st.title("📈 Sensores e previsões")
st.caption(
    "Evolução da dashboard da Fase 4: leituras dos sensores armazenadas no banco, "
    "métricas dos modelos de regressão, correlações e previsões agrícolas."
)

fase4_dashboard = common.load_fase4_dashboard()
fase4_dashboard.render_dashboard(show_title=False)
