"""
AWS Lambda "farmtech-monitor" - serviço de alerta da fazenda.

Recebe uma leitura dos sensores, avalia as regras agronômicas definidas pelo
grupo e, quando encontra problemas, publica no tópico Amazon SNS um e-mail
para os funcionários com os alertas e as ações corretivas sugeridas.

Os limites seguem as mesmas regras do ESP32 da Fase 4
(src/recommendation_engine.cpp), mantendo a consistência entre o campo
e a nuvem.

Variável de ambiente da Lambda:
    ALERT_TOPIC_ARN -> ARN do tópico SNS que envia os e-mails

Evento esperado:
    {
        "source": "sensors",
        "reading": {
            "soil_moisture": 22.0,
            "ph": 4.8,
            "nutrients_level": 35.0,
            "luminosity": 60.0,
            "temperature": 36.0,
            "air_humidity": 30.0,
            "productivity_index": 32.0,
            "irrigation_volume": 0.0,
            "created_at": "2026-11-05 14:30:00"
        }
    }
"""

import json
import os
from datetime import datetime, timedelta, timezone


FARM_NAME = "Fazenda FarmTech - Vinhedo/SP"

# Horário de Brasília, usado na mensagem enviada aos funcionários.
BRAZIL_TIMEZONE = timezone(timedelta(hours=-3))

SEVERITY_CRITICAL = "CRÍTICO"
SEVERITY_WARNING = "ATENÇÃO"

REQUIRED_FIELDS = [
    "soil_moisture",
    "ph",
    "nutrients_level",
    "temperature",
    "air_humidity",
    "productivity_index",
]

# ============================
# LIMITES (mesmos do ESP32)
# ============================

PH_MIN = 5.5
PH_MAX = 7.0
NUTRIENTS_MIN = 50.0
SOIL_MOISTURE_CRITICAL = 25.0
SOIL_MOISTURE_LOW = 40.0
EVAPORATION_TEMPERATURE = 35.0
EVAPORATION_AIR_HUMIDITY = 35.0
PRODUCTIVITY_LOW = 40.0


# ============================
# REGRAS DE ALERTA
# ============================

def evaluate_reading(reading):
    """
    Avalia a leitura e retorna a lista de alertas.
    Cada alerta contém severidade, problema identificado e ação corretiva.
    """
    alerts = []

    ph = float(reading["ph"])
    nutrients = float(reading["nutrients_level"])
    soil_moisture = float(reading["soil_moisture"])
    temperature = float(reading["temperature"])
    air_humidity = float(reading["air_humidity"])
    productivity = float(reading["productivity_index"])

    ph_adequate = PH_MIN <= ph <= PH_MAX
    nutrients_adequate = nutrients >= NUTRIENTS_MIN

    if ph < PH_MIN:
        alerts.append({
            "severity": SEVERITY_CRITICAL,
            "problem": f"pH do solo ácido ({ph:.1f}). Faixa ideal: {PH_MIN} a {PH_MAX}.",
            "action": (
                "Realizar calagem (aplicação de calcário) no talhão e "
                "suspender a irrigação até a correção do solo."
            ),
        })
    elif ph > PH_MAX:
        alerts.append({
            "severity": SEVERITY_CRITICAL,
            "problem": f"pH do solo alcalino ({ph:.1f}). Faixa ideal: {PH_MIN} a {PH_MAX}.",
            "action": (
                "Aplicar corretivo acidificante (ex.: enxofre elementar ou "
                "matéria orgânica) e suspender a irrigação até a correção do solo."
            ),
        })

    if not nutrients_adequate:
        alerts.append({
            "severity": SEVERITY_WARNING,
            "problem": f"Nível de nutrientes baixo ({nutrients:.1f}%). Mínimo: {NUTRIENTS_MIN:.0f}%.",
            "action": (
                "Realizar adubação NPK conforme a análise de solo antes "
                "de retomar a irrigação."
            ),
        })

    irrigation_note = ""

    if not ph_adequate or not nutrients_adequate:
        irrigation_note = (
            " Atenção: irrigar somente após corrigir o pH e/ou os nutrientes, "
            "conforme os alertas acima."
        )

    if soil_moisture < SOIL_MOISTURE_CRITICAL:
        alerts.append({
            "severity": SEVERITY_CRITICAL,
            "problem": f"Umidade do solo crítica ({soil_moisture:.1f}%).",
            "action": (
                "Acionar a irrigação imediatamente e verificar bomba, "
                "válvulas e linhas de gotejamento." + irrigation_note
            ),
        })
    elif soil_moisture < SOIL_MOISTURE_LOW:
        alerts.append({
            "severity": SEVERITY_WARNING,
            "problem": f"Umidade do solo baixa ({soil_moisture:.1f}%).",
            "action": (
                "Programar irrigação no próximo ciclo, preferencialmente "
                "no início da manhã ou no fim da tarde." + irrigation_note
            ),
        })

    if temperature >= EVAPORATION_TEMPERATURE and air_humidity <= EVAPORATION_AIR_HUMIDITY:
        alerts.append({
            "severity": SEVERITY_WARNING,
            "problem": (
                f"Risco de ressecamento: temperatura de {temperature:.1f} °C "
                f"e umidade do ar de {air_humidity:.1f}%."
            ),
            "action": (
                "Reforçar o monitoramento da umidade do solo e evitar "
                "irrigar nos horários mais quentes do dia."
            ),
        })

    if productivity < PRODUCTIVITY_LOW:
        alerts.append({
            "severity": SEVERITY_WARNING,
            "problem": f"Produtividade esperada baixa ({productivity:.1f}/100).",
            "action": (
                "Agendar vistoria técnica no talhão para revisar as "
                "condições agronômicas do cultivo."
            ),
        })

    return alerts


# ============================
# MENSAGEM
# ============================

def build_subject(alerts):
    # O assunto do SNS aceita apenas caracteres ASCII (sem acentos)
    # e no máximo 100 caracteres.
    critical_count = sum(1 for alert in alerts if alert["severity"] == SEVERITY_CRITICAL)
    level = "CRITICO" if critical_count else "ATENCAO"
    plural = "s" if len(alerts) > 1 else ""

    return f"[FarmTech] {level}: {len(alerts)} alerta{plural} na lavoura"


def build_message(reading, alerts):
    now = datetime.now(BRAZIL_TIMEZONE).strftime("%d/%m/%Y %H:%M:%S")
    reading_time = reading.get("created_at") or "-"

    lines = [
        f"{FARM_NAME}",
        "Alerta automático do sistema de monitoramento da lavoura",
        "",
        f"Alerta gerado em: {now} (horário de Brasília)",
        f"Leitura registrada em: {reading_time}",
        "",
        "LEITURA DOS SENSORES",
        "--------------------------------------",
        f"Umidade do solo: {float(reading['soil_moisture']):.1f}%",
        f"pH do solo: {float(reading['ph']):.1f}",
        f"Nível de nutrientes: {float(reading['nutrients_level']):.1f}%",
        f"Temperatura: {float(reading['temperature']):.1f} °C",
        f"Umidade do ar: {float(reading['air_humidity']):.1f}%",
        f"Produtividade esperada: {float(reading['productivity_index']):.1f}/100",
    ]

    if reading.get("luminosity") is not None:
        lines.append(f"Luminosidade: {float(reading['luminosity']):.1f}%")

    if reading.get("irrigation_volume") is not None:
        lines.append(f"Volume de irrigação calculado: {float(reading['irrigation_volume']):.1f} L")

    lines += ["", "ALERTAS E AÇÕES CORRETIVAS", "--------------------------------------"]

    for index, alert in enumerate(alerts, start=1):
        lines += [
            f"{index}. [{alert['severity']}] {alert['problem']}",
            f"   Ação sugerida: {alert['action']}",
            "",
        ]

    lines += [
        "--------------------------------------",
        "Mensagem enviada automaticamente pelo serviço FarmTech Monitor (AWS).",
    ]

    return "\n".join(lines)


# ============================
# HANDLER DA LAMBDA
# ============================

def validate_event(event):
    if not isinstance(event, dict) or not isinstance(event.get("reading"), dict):
        raise ValueError("Evento inválido: informe o campo 'reading' com a leitura dos sensores.")

    missing = [field for field in REQUIRED_FIELDS if event["reading"].get(field) is None]

    if missing:
        raise ValueError(f"Campos obrigatórios ausentes na leitura: {', '.join(missing)}")


def publish_alert(subject, message, sns_client=None):
    topic_arn = os.environ.get("ALERT_TOPIC_ARN")

    if not topic_arn:
        raise RuntimeError("Variável de ambiente ALERT_TOPIC_ARN não configurada na Lambda.")

    if sns_client is None:
        import boto3  # disponível no runtime Python da Lambda

        sns_client = boto3.client("sns")

    response = sns_client.publish(
        TopicArn=topic_arn,
        Subject=subject,
        Message=message,
    )

    return response["MessageId"]


def lambda_handler(event, context, sns_client=None):
    try:
        validate_event(event)
    except ValueError as error:
        return {"status": "error", "error": str(error)}

    reading = event["reading"]
    alerts = evaluate_reading(reading)

    if not alerts:
        return {
            "status": "ok",
            "alert_sent": False,
            "alerts": [],
            "message": "Leitura dentro dos parâmetros. Nenhum alerta enviado.",
        }

    subject = build_subject(alerts)
    message = build_message(reading, alerts)
    message_id = publish_alert(subject, message, sns_client=sns_client)

    print(json.dumps({
        "alert_sent": True,
        "message_id": message_id,
        "alerts": [alert["severity"] + " - " + alert["problem"] for alert in alerts],
    }, ensure_ascii=False))

    return {
        "status": "ok",
        "alert_sent": True,
        "message_id": message_id,
        "subject": subject,
        "alerts": alerts,
    }
