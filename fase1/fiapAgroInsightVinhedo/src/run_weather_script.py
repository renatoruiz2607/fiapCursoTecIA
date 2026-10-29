import subprocess

from constants import WEATHER_SCRIPT_PATH

def run_weather_script():
    try:
        result = subprocess.run(
            ["Rscript", WEATHER_SCRIPT_PATH],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return result.stdout

        return result.stderr

    except Exception as error:
        return str(error)