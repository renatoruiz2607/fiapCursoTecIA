"""
Dashboard integrada do sistema FarmTech.

Evolução da dashboard da Fase 4, agora na raiz do projeto, reunindo
os serviços das Fases 1, 2, 3, 4 e 6 e o serviço de alerta na AWS.

Execução:
    python launcher.py dashboard
    ou: streamlit run dashboard/app.py
"""

from pathlib import Path

import streamlit as st

VIEWS_DIR = Path(__file__).resolve().parent / "views"

st.set_page_config(
    page_title="FarmTech | Sistema Integrado",
    page_icon="🌱",
    layout="wide",
)

navigation = st.navigation(
    [
        st.Page(VIEWS_DIR / "overview.py", title="Visão geral", icon="🏠", default=True),
        st.Page(VIEWS_DIR / "sensors.py", title="Sensores e previsões", icon="📈"),
        st.Page(VIEWS_DIR / "services.py", title="Serviços", icon="🧰"),
        st.Page(VIEWS_DIR / "vision.py", title="Visão computacional", icon="📷"),
        st.Page(VIEWS_DIR / "alerts.py", title="Alertas AWS", icon="🔔"),
    ]
)

st.sidebar.caption("FarmTech Solutions · Sistema integrado das Fases 1 a 6")

navigation.run()
