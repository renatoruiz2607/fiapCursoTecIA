from pathlib import Path

import joblib
import pandas as pd

from database.sensor_reading_repository import get_latest_sensor_reading


TRAINED_MODELS_DIR = Path("ml/trained_models")

MODEL_FILES = {
    "soil_moisture": "soil_moisture_model.pkl",
    "ph": "ph_model.pkl",
    "nutrients_level": "nutrients_model.pkl",
    "productivity_index": "productivity_model.pkl",
    "irrigation_volume": "irrigation_model.pkl",
}


def load_model(model_file):
    model_path = TRAINED_MODELS_DIR / model_file

    if not model_path.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado: {model_path}. "
            "Execute o treinamento dos modelos primeiro."
        )

    return joblib.load(model_path)


def classify_fertilization_need(nutrients_level):
    if nutrients_level >= 80.0:
        return "Baixa"

    if nutrients_level >= 50.0:
        return "Média"

    return "Alta"


def generate_future_recommendation(predictions):
    ph = predictions["ph"]
    nutrients_level = predictions["nutrients_level"]
    soil_moisture = predictions["soil_moisture"]
    irrigation_volume = predictions["irrigation_volume"]
    productivity_index = predictions["productivity_index"]

    if ph < 5.5 or ph > 7.0:
        return "Corrigir o pH do solo antes de realizar novas ações de irrigação."

    if nutrients_level < 50.0:
        return "Realizar fertilização antes de irrigar, pois o nível de nutrientes previsto está baixo."

    if irrigation_volume >= 7.0:
        return "Irrigação urgente recomendada com base na previsão do modelo."

    if irrigation_volume >= 4.0:
        return "Irrigação recomendada com base na previsão do modelo."

    if irrigation_volume > 0.0:
        return "Irrigação leve recomendada para manter a estabilidade do solo."

    if productivity_index < 40.0:
        return "Produtividade prevista baixa. Revisar condições agronômicas do cultivo."

    if soil_moisture < 40.0:
        return "Monitorar umidade do solo, pois há tendência de baixa umidade."

    return "Condições previstas adequadas. Nenhuma ação imediata necessária."


def execute_agricultural_prediction():
    latest_reading = get_latest_sensor_reading()

    if not latest_reading:
        print("\nNenhum registro encontrado no banco de dados.")
        print("Salve leituras ou importe o CSV simulado antes de executar a previsão.")
        return

    models = {
        target: load_model(model_file)
        for target, model_file in MODEL_FILES.items()
    }

    predictions = {}

    for target, model in models.items():
        feature_columns = model.named_steps["preprocessamento"].transformers_[0][2]

        input_data = pd.DataFrame(
            [{column: latest_reading[column] for column in feature_columns}]
        )

        prediction = model.predict(input_data)[0]
        predictions[target] = round(float(prediction), 2)

    fertilization_need = classify_fertilization_need(
        predictions["nutrients_level"]
    )

    future_recommendation = generate_future_recommendation(predictions)

    print("\n======================================")
    print(" PREVISÃO AGRÍCOLA")
    print("======================================")
    print("\nBase utilizada:")
    print("Última leitura registrada no banco de dados.")

    print("\nResultados previstos:")
    print("--------------------------------------")
    print(f"Umidade prevista: {predictions['soil_moisture']:.1f}%")
    print(f"pH previsto: {predictions['ph']:.1f}")
    print(f"Nível de nutrientes previsto: {predictions['nutrients_level']:.1f}%")
    print(f"Produtividade prevista: {predictions['productivity_index']:.1f}/100")
    print(f"Volume de irrigação previsto: {predictions['irrigation_volume']:.1f} L")

    print("\nManejo agrícola:")
    print("--------------------------------------")
    print(f"Necessidade de fertilização: {fertilization_need}")

    print("\nRecomendação futura:")
    print("--------------------------------------")
    print(future_recommendation)