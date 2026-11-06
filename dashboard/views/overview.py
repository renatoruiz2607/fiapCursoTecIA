import streamlit as st

import common
import launcher

st.title("🌱 FarmTech — Sistema Integrado")
st.caption(
    "Consolidação dos serviços desenvolvidos nas Fases 1 a 6 em um único sistema, "
    "com monitoramento dos sensores, Machine Learning, visão computacional e alertas na AWS."
)

# ============================
# STATUS
# ============================

summary = common.get_database_summary()
vision_status = common.vision_models_status()
vision_ready = sum(vision_status.values())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Leituras no banco", summary["total"])
col2.metric("Modelos de ML (Fase 4)", "Treinados" if common.models_trained() else "Pendentes")
col3.metric("Modelos de visão (Fase 6)", f"{vision_ready} de {len(vision_status)}")
col4.metric("Alertas AWS", "Configurados" if common.aws_configured() else "Pendentes")

latest = summary["latest"]

if latest:
    st.caption(
        f"Última leitura: registro {latest['id']} em {latest['created_at']} · "
        f"umidade {latest['soil_moisture']:.1f}% · pH {latest['ph']:.1f} · "
        f"nutrientes {latest['nutrients_level']:.1f}%"
    )
else:
    st.info("Nenhuma leitura no banco. Importe o CSV simulado na página Serviços (Fase 4).")

# ============================
# ARQUITETURA
# ============================

st.subheader("Fluxo de dados do sistema")

st.graphviz_chart(
    """
    digraph {
        rankdir=LR;
        bgcolor="transparent";
        node [shape=box, style="rounded,filled", fillcolor="#eef6fb", color="#1d5f8c",
              fontname="Helvetica", fontsize=11];
        edge [color="#7a8a99", fontname="Helvetica", fontsize=9];

        f1 [label="Fase 1\\nAgro Insight Vinhedo\\nPython + R"];
        f2 [label="Fase 2\\nSensores ESP32 (Wokwi)\\nprevisão de chuva"];
        f3 [label="Fase 3\\nBanco de dados\\nSQLite"];
        f4 [label="Fase 4\\nMachine Learning\\nprevisões"];
        f6 [label="Fase 6\\nVisão computacional\\nYOLOv5 + CNN"];
        dash [label="Dashboard integrada\\n+ launcher", fillcolor="#eef8f0", color="#1f6f50"];
        aws [label="AWS (Fase 5)\\nLambda + SNS", fillcolor="#fff8e8", color="#8a6200"];
        mail [label="E-mail dos\\nfuncionários", shape=note, fillcolor="#f6f7f9", color="#3f4a56"];

        f2 -> f3 [label="leituras"];
        f3 -> f4 [label="histórico"];
        f3 -> aws [label="última leitura"];
        aws -> mail [label="alertas e ações"];
        f1 -> dash; f4 -> dash; f6 -> dash; f3 -> dash;
    }
    """,
    width="stretch",
)

# ============================
# SERVIÇOS POR FASE
# ============================

st.subheader("Serviços disponíveis")

kind_labels = {
    launcher.KIND_TASK: "Executa e exibe o resultado",
    launcher.KIND_INTERACTIVE: "Menu interativo no terminal",
    launcher.KIND_SERVER: "Abre no navegador",
}

rows = [
    {
        "Fase": f"{service.phase} · {launcher.PHASES[service.phase]}",
        "Serviço": service.name,
        "Tipo": kind_labels[service.kind],
        "Comando no terminal": f"python launcher.py run {service.key}",
    }
    for service in launcher.SERVICES
    if service.phase != "Dashboard"
]

st.dataframe(rows, width="stretch", hide_index=True)

st.caption(
    "Todos os serviços podem ser disparados pela página Serviços ou pelo terminal, "
    "com `python launcher.py` (menu por fase) ou com os comandos acima."
)
