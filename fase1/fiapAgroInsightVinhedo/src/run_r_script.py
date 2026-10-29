import subprocess

from constants import R_SCRIPT_PATH

def run_r_script():
    try:
        result = subprocess.run(
            ["Rscript", R_SCRIPT_PATH],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr

    except Exception as error:
        return str(error)