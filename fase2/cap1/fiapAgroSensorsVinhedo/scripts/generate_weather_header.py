from pathlib import Path

Import("env")

from weather_api import (
    CITY_NAME,
    get_api_key,
    build_forecast_url,
    fetch_weather_forecast,
    analyze_rain_conditions,
    calculate_rain_forecast_level,
)

PROJECT_DIR = Path(env["PROJECT_DIR"])
SRC_DIR = PROJECT_DIR / "src"
OUTPUT_HEADER_PATH = SRC_DIR / "generated_weather_data.h"

def escape_cpp_string(value: str) -> str:
    """
    Escapes double quotes for safe use inside a C++ string literal.
    """
    return value.replace("\\", "\\\\").replace('"', '\\"')

def generate_header_content(
    city_name: str,
    rain_forecast_level: int,
    max_rain_probability_percent: float,
    max_rain_volume_mm: float,
    rain_forecast_text: str,
) -> str:
    """
    Builds the C++ header content with the weather data generated at build time.
    """
    escaped_city_name = escape_cpp_string(city_name)
    escaped_rain_forecast_text = escape_cpp_string(rain_forecast_text)

    return f"""#pragma once

const int DEFAULT_RAIN_FORECAST_LEVEL = {rain_forecast_level};
const float DEFAULT_MAX_RAIN_PROBABILITY_PERCENT = {max_rain_probability_percent:.2f}f;
const float DEFAULT_MAX_RAIN_VOLUME_MM = {max_rain_volume_mm:.2f}f;

const char DEFAULT_WEATHER_CITY[] = "{escaped_city_name}";
const char DEFAULT_RAIN_FORECAST_TEXT[] = "{escaped_rain_forecast_text}";
"""

def main() -> None:
    print("Running weather pre-build step...")

    api_key = get_api_key()
    url = build_forecast_url(CITY_NAME, api_key)

    forecast_data = fetch_weather_forecast(url)
    analysis = analyze_rain_conditions(forecast_data)

    forecast_level = calculate_rain_forecast_level(analysis)

    city = forecast_data.get("city", {}).get("name", "Unknown")
    country = forecast_data.get("city", {}).get("country", "Unknown")
    full_city_name = f"{city}, {country}"

    rain_forecast_text = (
        "RAIN EXPECTED"
        if forecast_level == 1
        else "NO RAIN"
    )

    header_content = generate_header_content(
        city_name=full_city_name,
        rain_forecast_level=forecast_level,
        max_rain_probability_percent=analysis["max_pop"] * 100,
        max_rain_volume_mm=analysis["max_rain_volume"],
        rain_forecast_text=rain_forecast_text,
    )

    OUTPUT_HEADER_PATH.write_text(header_content, encoding="utf-8")

    print(f"=== WEATHER API RESULT ==")
    print(f"Weather header generated at: {OUTPUT_HEADER_PATH}")
    print(f"City: {full_city_name}")
    print(f"Rain forecast level: {forecast_level}")
    print(f"Max rain probability: {analysis['max_pop'] * 100:.2f}%")
    print(f"Max rain volume: {analysis['max_rain_volume']:.2f} mm\n")

main()