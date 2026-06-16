import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from ml.dataset_builder import load_sensor_dataset
from ml.prediction_service import (
    MODEL_FILES,
    TRAINED_MODELS_DIR,
    classify_fertilization_need,
    generate_future_recommendation,
)


METRICS_PATH = Path("ml/metrics.json")


st.set_page_config(
    page_title="AgroSensorsIntelligence",
    layout="wide"
)


st.markdown(
    """
    <style>
        .section-title {
            font-size: 1.6rem;
            font-weight: 700;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            padding: 0.8rem 1rem;
            border-radius: 12px;
        }

        .section-title-blue {
            color: #1d5f8c;
            background-color: #eef6fb;
        }

        .section-title-green {
            color: #1f6f50;
            background-color: #eef8f0;
        }

        .section-title-yellow {
            color: #8a6200;
            background-color: #fff8e8;
        }

        .section-title-purple {
            color: #5d3c8c;
            background-color: #f5f0fb;
        }

        .section-title-gray {
            color: #3f4a56;
            background-color: #f6f7f9;
        }

        [data-testid="stMetricValue"] {
            color: #516582;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_metrics():
    if not METRICS_PATH.exists():
        return None

    with open(METRICS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def run_predictions(latest_reading):
    models = {
        target: joblib.load(TRAINED_MODELS_DIR / model_file)
        for target, model_file in MODEL_FILES.items()
    }

    predictions = {}

    for target, model in models.items():
        feature_columns = model.named_steps["preprocessamento"].transformers_[0][2]

        input_data = pd.DataFrame(
            [{column: latest_reading[column] for column in feature_columns}]
        )

        predictions[target] = round(float(model.predict(input_data)[0]), 2)

    return predictions


st.title("🧠 AgroSensorsIntelligence")
st.caption("Dashboard analítico com sensores, Machine Learning e recomendações agrícolas.")

df = load_sensor_dataset()
metrics = load_metrics()

if df.empty:
    st.warning("Nenhum dado encontrado no banco. Importe o CSV simulado ou salve leituras dos sensores.")
    st.stop()

latest_reading = df.iloc[-1].to_dict()

st.markdown(
    '<div class="section-title section-title-green">Visão geral do banco</div>',
    unsafe_allow_html=True,
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Registros", len(df))
col2.metric("Umidade média", f"{df['soil_moisture'].mean():.1f}%")
col3.metric("pH médio", f"{df['ph'].mean():.1f}")
col4.metric("Nível médio de nutrientes", f"{df['nutrients_level'].mean():.1f}%")
col5.metric("Produtividade média", f"{df['productivity_index'].mean():.1f}/100")

st.markdown(
    '<div class="section-title section-title-blue">Última leitura registrada</div>',
    unsafe_allow_html=True,
)

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Umidade do solo", f"{latest_reading['soil_moisture']:.1f}%")
col2.metric("pH", f"{latest_reading['ph']:.1f}")
col3.metric("Nutrientes", f"{latest_reading['nutrients_level']:.1f}%")
col4.metric("Luminosidade", f"{latest_reading['luminosity']:.1f}%")
col5.metric("Temperatura", f"{latest_reading['temperature']:.1f} °C")
col6.metric("Umidade do ar", f"{latest_reading['air_humidity']:.1f}%")

st.markdown(
    '<div class="section-title section-title-purple">Métricas dos modelos de regressão</div>',
    unsafe_allow_html=True,
)

if not metrics:
    st.warning("Métricas não encontradas. Execute o treinamento dos modelos pelo menu.")
else:
    metric_cols = st.columns(len(metrics))

    for index, (_, model_data) in enumerate(metrics.items()):
        with metric_cols[index]:
            st.subheader(model_data["label"])
            st.metric("MAE", model_data["metrics"]["mae"])
            st.metric("MSE", model_data["metrics"]["mse"])
            st.metric("RMSE", model_data["metrics"]["rmse"])
            st.metric("R²", model_data["metrics"]["r2"])

st.markdown(
    '<div class="section-title section-title-yellow">Gráficos de correlação</div>',
    unsafe_allow_html=True,
)

numeric_df = df[
    [
        "soil_moisture",
        "ph",
        "nutrients_level",
        "luminosity",
        "temperature",
        "air_humidity",
        "productivity_index",
        "irrigation_volume",
    ]
]

correlation = numeric_df.corr()

st.dataframe(correlation, use_container_width=True)
st.bar_chart(correlation["productivity_index"].drop("productivity_index"))

st.markdown(
    '<div class="section-title section-title-green">Resultados de previsão</div>',
    unsafe_allow_html=True,
)

try:
    predictions = run_predictions(latest_reading)

    fertilization_need = classify_fertilization_need(
        predictions["nutrients_level"]
    )

    future_recommendation = generate_future_recommendation(predictions)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Umidade prevista", f"{predictions['soil_moisture']:.1f}%")
    col2.metric("pH previsto", f"{predictions['ph']:.1f}")
    col3.metric("Nutrientes previstos", f"{predictions['nutrients_level']:.1f}%")
    col4.metric("Produtividade prevista", f"{predictions['productivity_index']:.1f}/100")
    col5.metric("Irrigação prevista", f"{predictions['irrigation_volume']:.1f} L")

    st.subheader("Manejo agrícola previsto")
    st.write(f"Necessidade de fertilização: **{fertilization_need}**")

    st.subheader("Recomendação futura")
    st.write(future_recommendation)

except FileNotFoundError:
    st.warning("Modelos treinados não encontrados. Execute o treinamento dos modelos pelo menu.")

st.markdown(
    '<div class="section-title section-title-blue">Tendência de produtividade</div>',
    unsafe_allow_html=True,
)

st.line_chart(df["productivity_index"])

st.caption(
    "As previsões são geradas a partir dos modelos treinados com o histórico armazenado no banco Oracle. "
    "A última leitura registrada é utilizada como cenário atual para estimar as condições agrícolas futuras."
)