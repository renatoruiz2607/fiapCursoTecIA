import streamlit as st

import common
from alert_client import TEST_READING, get_latest_reading, invoke_monitor
from lambda_function import (
    SEVERITY_CRITICAL,
    build_message,
    build_subject,
    evaluate_reading,
)

st.title("🔔 Alertas AWS")
st.caption(
    "Serviço de mensageria na AWS: a Lambda farmtech-monitor avalia a leitura dos sensores "
    "e, quando encontra problemas, envia por e-mail (Amazon SNS) os alertas e as ações corretivas."
)

if not common.aws_configured():
    st.warning(
        "Credenciais AWS não configuradas no .env. A prévia funciona normalmente, "
        "mas o envio exige AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY e AWS_DEFAULT_REGION.",
        icon="⚠️",
    )


def show_alerts(reading):
    alerts = evaluate_reading(reading)

    if not alerts:
        st.success("Leitura dentro dos parâmetros. Nenhum alerta seria enviado.")
        return alerts

    for alert in alerts:
        message = f"**{alert['problem']}**  \nAção sugerida: {alert['action']}"

        if alert["severity"] == SEVERITY_CRITICAL:
            st.error(message, icon="🚨")
        else:
            st.warning(message, icon="⚠️")

    with st.expander("Prévia do e-mail"):
        st.markdown(f"**Assunto:** {build_subject(alerts)}")
        st.code(build_message(reading, alerts), language="text")

    return alerts


def send_alert(reading, result_key):
    with st.spinner("Enviando leitura ao serviço de monitoramento na AWS..."):
        try:
            st.session_state[result_key] = {"ok": True, "result": invoke_monitor(reading)}
        except ModuleNotFoundError:
            st.session_state[result_key] = {
                "ok": False,
                "error": "Pacote boto3 não instalado. Execute: pip install -r requirements.txt",
            }
        except Exception as error:
            st.session_state[result_key] = {"ok": False, "error": str(error)}


def show_send_result(result_key):
    state = st.session_state.get(result_key)

    if not state:
        return

    if not state["ok"]:
        st.error(f"Não foi possível enviar o alerta: {state['error']}")
        return

    result = state["result"]

    if result.get("status") == "error":
        st.error(f"A Lambda recusou a leitura: {result.get('error')}")
    elif result.get("alert_sent"):
        st.success(
            f"Alerta enviado por e-mail. Assunto: {result['subject']} · "
            f"ID da mensagem (SNS): {result['message_id']}"
        )
    else:
        st.info(result.get("message", "Nenhum alerta enviado."))


tab_latest, tab_simulation = st.tabs(["Última leitura do banco", "Simular leitura"])

# ============================
# ÚLTIMA LEITURA
# ============================

with tab_latest:
    reading = get_latest_reading()

    if not reading:
        st.info("Nenhuma leitura no banco. Importe o CSV ou salve uma leitura pela Fase 4.")
    else:
        st.caption(f"Registro {reading['id']} · {reading['created_at']}")

        cols = st.columns(6)
        cols[0].metric("Umidade do solo", f"{reading['soil_moisture']:.1f}%")
        cols[1].metric("pH", f"{reading['ph']:.1f}")
        cols[2].metric("Nutrientes", f"{reading['nutrients_level']:.1f}%")
        cols[3].metric("Temperatura", f"{reading['temperature']:.1f} °C")
        cols[4].metric("Umidade do ar", f"{reading['air_humidity']:.1f}%")
        cols[5].metric("Produtividade", f"{reading['productivity_index']:.1f}")

        alerts = show_alerts(reading)

        if st.button("Enviar alerta da última leitura", type="primary", disabled=not alerts):
            send_alert(reading, "latest_result")

        show_send_result("latest_result")

# ============================
# SIMULAÇÃO
# ============================

with tab_simulation:
    st.caption(
        "Ajuste os valores dos sensores para simular uma situação no campo e enviar o alerta. "
        "A leitura simulada não é gravada no banco."
    )

    defaults = TEST_READING

    col1, col2, col3 = st.columns(3)

    simulated = {
        "soil_moisture": col1.slider("Umidade do solo (%)", 0.0, 100.0, defaults["soil_moisture"], 0.5),
        "ph": col1.slider("pH do solo", 3.0, 9.0, defaults["ph"], 0.1),
        "nutrients_level": col2.slider("Nível de nutrientes (%)", 0.0, 100.0, defaults["nutrients_level"], 0.5),
        "productivity_index": col2.slider("Produtividade esperada", 0.0, 100.0, defaults["productivity_index"], 0.5),
        "temperature": col3.slider("Temperatura (°C)", 0.0, 50.0, defaults["temperature"], 0.5),
        "air_humidity": col3.slider("Umidade do ar (%)", 0.0, 100.0, defaults["air_humidity"], 0.5),
        "created_at": "leitura simulada pela dashboard",
    }

    alerts = show_alerts(simulated)

    if st.button("Enviar alerta da leitura simulada", type="primary", disabled=not alerts):
        send_alert(simulated, "simulation_result")

    show_send_result("simulation_result")
