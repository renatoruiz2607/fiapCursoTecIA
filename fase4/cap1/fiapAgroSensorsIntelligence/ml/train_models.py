import json
from pathlib import Path

import joblib
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ml.dataset_builder import load_sensor_dataset, validate_dataset


TRAINED_MODELS_DIR = Path("ml/trained_models")
METRICS_PATH = Path("ml/metrics.json")

TARGETS = {
    "soil_moisture": {
        "label": "Umidade do solo",
        "model_file": "soil_moisture_model.pkl",
    },
    "ph": {
        "label": "pH do solo",
        "model_file": "ph_model.pkl",
    },
    "nutrients_level": {
        "label": "Nível de nutrientes",
        "model_file": "nutrients_model.pkl",
    },
    "productivity_index": {
        "label": "Produtividade esperada",
        "model_file": "productivity_model.pkl",
    },
    "irrigation_volume": {
        "label": "Volume de irrigação",
        "model_file": "irrigation_model.pkl",
    },
}

FEATURE_COLUMNS = [
    "soil_moisture",
    "ph",
    "nutrients_level",
    "luminosity",
    "temperature",
    "air_humidity",
    "productivity_index",
    "irrigation_volume",
]


def build_pipeline(feature_columns):
    numeric_pipeline = Pipeline(
        steps=[
            ("imputar", SimpleImputer(strategy="mean")),
            ("padronizar", StandardScaler()),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numerica", numeric_pipeline, feature_columns)
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessamento", preprocessor),
            ("regressor", RandomForestRegressor(
                n_estimators=100,
                random_state=42
            )),
        ]
    )

    return pipeline


def evaluate_model(y_test, predictions):
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    return {
        "mae": round(mae, 4),
        "mse": round(mse, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4),
    }


def train_single_model(dataframe, target_column, config):
    feature_columns = [
        column for column in FEATURE_COLUMNS
        if column != target_column
    ]

    x = dataframe[feature_columns]
    y = dataframe[target_column]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42
    )

    pipeline = build_pipeline(feature_columns)

    model = pipeline.fit(x_train, y_train)
    predictions = model.predict(x_test)

    metrics = evaluate_model(y_test, predictions)

    model_path = TRAINED_MODELS_DIR / config["model_file"]
    joblib.dump(model, model_path)

    return {
        "target": target_column,
        "label": config["label"],
        "model_file": str(model_path),
        "features": feature_columns,
        "metrics": metrics,
    }


def train_all_models():
    TRAINED_MODELS_DIR.mkdir(parents=True, exist_ok=True)

    dataframe = load_sensor_dataset()
    validate_dataset(dataframe)

    metrics_result = {}

    print("\nIniciando treinamento dos modelos de regressão...")

    for target_column, config in TARGETS.items():
        print(f"\nTreinando modelo: {config['label']}")

        result = train_single_model(
            dataframe=dataframe,
            target_column=target_column,
            config=config
        )

        metrics_result[target_column] = result

        print("Métricas:")
        print(f"MAE: {result['metrics']['mae']}")
        print(f"MSE: {result['metrics']['mse']}")
        print(f"RMSE: {result['metrics']['rmse']}")
        print(f"R²: {result['metrics']['r2']}")

    with open(METRICS_PATH, "w", encoding="utf-8") as file:
        json.dump(metrics_result, file, indent=4, ensure_ascii=False)

    print("\nTreinamento concluído com sucesso.")
    print(f"Modelos salvos em: {TRAINED_MODELS_DIR}")
    print(f"Métricas salvas em: {METRICS_PATH}")


if __name__ == "__main__":
    train_all_models()