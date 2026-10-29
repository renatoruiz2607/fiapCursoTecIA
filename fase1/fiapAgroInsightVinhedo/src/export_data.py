import csv

from data_store import list_records
from constants import CSV_FILE_PATH

def export_records_to_csv():
    records = list_records()

    if not records:
        return False

    with open(CSV_FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "crop_type",
            "width_meters",
            "length_meters",
            "area",
            "input_type",
            "input_dosage",
            "total_input",
            "row_spacing_meters",
            "row_count",
            "total_row_length"
        ])

        writer.writerows(records)

    return True