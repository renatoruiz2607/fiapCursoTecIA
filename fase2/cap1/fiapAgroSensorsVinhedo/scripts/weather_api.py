import json
import os
import sys
import urllib.parse
import urllib.request

# ============================
# CONFIGURATION
# ============================

API_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
# FIXME - voltar cidade,país para Vinhedo,BR
CITY_NAME = "Ipiranga,BR"

FORECAST_WINDOW_COUNT = 8  # next 24h (8 * 3h)

# Agricultural decision rule
MIN_RAIN_PROBABILITY = 0.60  # 60%
MIN_RAIN_VOLUME_MM = 2.0     # 2mm in 3h

# ============================
# API ACCESS
# ============================

def get_api_key() -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        raise ValueError(
            "Environment variable OPENWEATHER_API_KEY not found."
        )

    return api_key

def build_forecast_url(city_name: str, api_key: str) -> str:
    query_params = urllib.parse.urlencode({
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    })

    return f"{API_BASE_URL}?{query_params}"

def fetch_weather_forecast(url: str) -> dict:
    with urllib.request.urlopen(url) as response:
        if response.status != 200:
            raise RuntimeError(
                f"Request failed with status {response.status}"
            )

        body = response.read().decode("utf-8")
        return json.loads(body)

# ============================
# BUSINESS LOGIC
# ============================

def analyze_rain_conditions(forecast_data: dict) -> dict:
    """
    Analyzes upcoming periods and returns relevant metrics.
    """

    forecast_list = forecast_data.get("list", [])
    next_periods = forecast_list[:FORECAST_WINDOW_COUNT]

    max_pop = 0.0
    max_rain_volume = 0.0
    relevant_rain_found = False

    for period in next_periods:
        pop = period.get("pop", 0.0)

        rain_data = period.get("rain", {})
        rain_volume = rain_data.get("3h", 0.0)

        # Atualiza máximos para log
        if pop > max_pop:
            max_pop = pop

        if rain_volume > max_rain_volume:
            max_rain_volume = rain_volume

        # Main rule
        if pop >= MIN_RAIN_PROBABILITY and rain_volume >= MIN_RAIN_VOLUME_MM:
            relevant_rain_found = True

    return {
        "relevant_rain_found": relevant_rain_found,
        "max_pop": max_pop,
        "max_rain_volume": max_rain_volume
    }

def calculate_rain_forecast_level(analysis: dict) -> int:
    """
    Converts analysis to simple value for ESP32.
    """
    return 1 if analysis["relevant_rain_found"] else 0

# ============================
# OUTPUT
# ============================

def print_summary(forecast_data: dict, analysis: dict, forecast_level: int) -> None:
    city = forecast_data.get("city", {}).get("name", "Unknown")
    country = forecast_data.get("city", {}).get("country", "Unknown")

    print("=== WEATHER FORECAST SUMMARY ===")
    print(f"Location: {city}, {country}")
    print("Forecast window: next 24 hours")
    print()

    print("=== ANALYSIS ===")
    print(f"Relevant rain found: {'YES' if analysis['relevant_rain_found'] else 'NO'}")

    max_pop_percent = analysis['max_pop'] * 100
    print(f"Max probability of rain: {max_pop_percent:.2f}%")
    print(f"Max rain volume (3h): {analysis['max_rain_volume']:.2f} mm")
    print()

    print("=== ESP32 SERIAL INPUT ===")
    print(f"Type this value in the serial monitor: {forecast_level}")
    print()

    print("Legend:")
    print("1 = relevant rain → irrigation OFF")
    print("0 = no relevant rain → irrigation can proceed")

# ============================
# MAIN
# ============================

def main():
    try:
        api_key = get_api_key()
        url = build_forecast_url(CITY_NAME, api_key)

        forecast_data = fetch_weather_forecast(url)

        analysis = analyze_rain_conditions(forecast_data)

        forecast_level = calculate_rain_forecast_level(analysis)

        print_summary(forecast_data, analysis, forecast_level)

    except Exception as error:
        print("Failed to retrieve weather data.")
        print(f"Error: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()