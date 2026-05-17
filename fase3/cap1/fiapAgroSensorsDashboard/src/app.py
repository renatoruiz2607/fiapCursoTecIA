import streamlit as st

# ============================
# PAGE CONFIGURATION
# ============================

st.set_page_config(
    page_title="Agro Sensors Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================
# PAGE HEADER
# ============================

st.title("📊 Agro Sensors Dashboard")

st.write(
    """
    Dashboard desenvolvido para visualizar dados de irrigação na agricultura,
    incluindo umidade do solo, pH do solo, níveis de nutrientes e decisões de irrigação.
    """
)

# ============================
# INITIAL CONTENT
# ============================

st.info("Dashboard inicializado com sucesso.")