import re
import subprocess
from pathlib import Path

Import("env")

PROJECT_DIR = Path(env["PROJECT_DIR"])
SRC_DIR = PROJECT_DIR / "src"
OUTPUT_HEADER_PATH = SRC_DIR / "generated_irrigation_model_data.h"

# ============================
# DEFAULT INPUT VALUES
# ============================

DEFAULT_SOIL_MOISTURE = 40.0
DEFAULT_PH_VALUE = 6.1
DEFAULT_ACTIVE_NUTRIENTS = 3
DEFAULT_POTASSIUM_OK = 1
DEFAULT_RAIN_FORECAST_LEVEL = 0

def escape_cpp_string(value: str) -> str:
    """
    Escapes text for safe use inside a C++ string literal.
    """
    return value.replace("\\", "\\\\").replace('"', '\\"')

def run_irrigation_model() -> tuple[float, int]:
    """
    Executes the R script and returns:
    - irrigation probability
    - irrigation decision
    """
    command = [
        "Rscript",
        str(PROJECT_DIR / "scripts" / "irrigation_model.R"),
        str(DEFAULT_SOIL_MOISTURE),
        str(DEFAULT_PH_VALUE),
        str(DEFAULT_ACTIVE_NUTRIENTS),
        str(DEFAULT_POTASSIUM_OK),
        str(DEFAULT_RAIN_FORECAST_LEVEL),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
        cwd=PROJECT_DIR
    )

    output = result.stdout

    probability_match = re.search(r"Irrigation probability:\s*([0-9.]+)", output)
    decision_match = re.search(r"Irrigation decision:\s*([0-9]+)", output)

    if not probability_match or not decision_match:
        raise ValueError(
            "Failed to parse irrigation model output.\n"
            f"R output was:\n{output}"
        )

    probability = float(probability_match.group(1))
    decision = int(decision_match.group(1))

    return probability, decision

def generate_header_content(
    soil_moisture: float,
    ph_value: float,
    active_nutrients: int,
    potassium_ok: int,
    rain_forecast_level: int,
    irrigation_probability: float,
    irrigation_decision: int,
) -> str:
    """
    Generates the C++ header content with the R model result.
    """
    irrigation_text = "IRRIGATE" if irrigation_decision == 1 else "DO NOT IRRIGATE"
    escaped_irrigation_text = escape_cpp_string(irrigation_text)

    return f"""#pragma once

const float DEFAULT_R_MODEL_SOIL_MOISTURE = {soil_moisture:.2f}f;
const float DEFAULT_R_MODEL_PH_VALUE = {ph_value:.2f}f;
const int DEFAULT_R_MODEL_ACTIVE_NUTRIENTS = {active_nutrients};
const int DEFAULT_R_MODEL_POTASSIUM_OK = {potassium_ok};
const int DEFAULT_R_MODEL_RAIN_FORECAST_LEVEL = {rain_forecast_level};

const float DEFAULT_R_MODEL_IRRIGATION_PROBABILITY = {irrigation_probability:.4f}f;
const int DEFAULT_R_MODEL_IRRIGATION_DECISION = {irrigation_decision};

const char DEFAULT_R_MODEL_IRRIGATION_TEXT[] = "{escaped_irrigation_text}";
"""

def main() -> None:
    print("Running irrigation model pre-build step...")

    probability, decision = run_irrigation_model()

    header_content = generate_header_content(
        soil_moisture=DEFAULT_SOIL_MOISTURE,
        ph_value=DEFAULT_PH_VALUE,
        active_nutrients=DEFAULT_ACTIVE_NUTRIENTS,
        potassium_ok=DEFAULT_POTASSIUM_OK,
        rain_forecast_level=DEFAULT_RAIN_FORECAST_LEVEL,
        irrigation_probability=probability,
        irrigation_decision=decision,
    )

    OUTPUT_HEADER_PATH.write_text(header_content, encoding="utf-8")

    print(f"=== IRRIGATION TRAINING RESULT ===")
    print(f"Irrigation model header generated at: {OUTPUT_HEADER_PATH}")
    print(f"Soil moisture: {DEFAULT_SOIL_MOISTURE}")
    print(f"pH value: {DEFAULT_PH_VALUE}")
    print(f"Active nutrients: {DEFAULT_ACTIVE_NUTRIENTS}")
    print(f"Potassium OK: {DEFAULT_POTASSIUM_OK}")
    print(f"Rain forecast level: {DEFAULT_RAIN_FORECAST_LEVEL}")
    print(f"Irrigation probability: {probability:.4f}")
    print(f"Irrigation decision: {decision}")


main()