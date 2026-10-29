from menu import get_menu_option
from crop_data import create_record
from data_store import add_record, list_records, update_record, delete_record
from export_data import export_records_to_csv
from run_r_script import run_r_script
from run_weather_script import run_weather_script
from constants import (
    MENU_ADD,
    MENU_LIST,
    MENU_UPDATE,
    MENU_DELETE,
    MENU_EXPORT,
    MENU_RUN_R,
    MENU_RUN_WEATHER,
    MENU_EXIT,
    INVALID_OPTION_MESSAGE,
    EMPTY_RECORDS_MESSAGE,
    INVALID_INDEX_MESSAGE,
    RECORD_ADDED_MESSAGE,
    RECORD_UPDATED_MESSAGE,
    RECORD_DELETED_MESSAGE,
    EXIT_MESSAGE,
    ENTER_UPDATE_INDEX_MESSAGE,
    ENTER_DELETE_INDEX_MESSAGE,
    INDEX_CROP_TYPE,
    INDEX_WIDTH_METERS,
    INDEX_LENGTH_METERS,
    INDEX_AREA,
    INDEX_INPUT_TYPE,
    INDEX_INPUT_DOSAGE,
    INDEX_TOTAL_INPUT,
    INDEX_ROW_SPACING_METERS,
    INDEX_ROW_COUNT,
    INDEX_TOTAL_ROW_LENGTH,
    EXPORT_SUCCESS_MESSAGE,
    NO_DATA_TO_EXPORT_MESSAGE,
    WEATHER_SCRIPT_OUTPUT_TITLE
)

def show_records():
    records = list_records()

    if not records:
        print(EMPTY_RECORDS_MESSAGE)
        return

    for index, record in enumerate(records):
        crop_type = record[INDEX_CROP_TYPE]
        width = record[INDEX_WIDTH_METERS]
        length = record[INDEX_LENGTH_METERS]
        area = record[INDEX_AREA]
        input_type = record[INDEX_INPUT_TYPE]
        input_dosage = record[INDEX_INPUT_DOSAGE]
        total_input = record[INDEX_TOTAL_INPUT]

        row_spacing = record[INDEX_ROW_SPACING_METERS]
        row_count = record[INDEX_ROW_COUNT]
        total_row_length = record[INDEX_TOTAL_ROW_LENGTH]

        # Tratamento de None → "N/A"
        area = area if area is not None else "N/A"
        total_input = f"{total_input:.2f}" if total_input != "N/A" else "N/A"
        row_spacing = row_spacing if row_spacing is not None else "N/A"
        row_count = row_count if row_count is not None else "N/A"
        total_row_length = total_row_length if total_row_length is not None else "N/A"

        print(f"\n{index} - Crop: {crop_type} | Width: {width} m | Length: {length} m")
        print(f"    Area: {area} | Input: {input_type} | Dosage: {input_dosage} | Total Input: {total_input}")

        # Só mostra dados de uva se existir
        if row_spacing != "N/A":
            print(f"    Row Spacing: {row_spacing} m | Row Count: {row_count} | Total Row Length: {total_row_length}")

def main():
    while True:
        option = get_menu_option()

        if option == MENU_ADD:
            record = create_record()
            if record is not None:
                add_record(record)
                print(RECORD_ADDED_MESSAGE)

        elif option == MENU_LIST:
            show_records()

        elif option == MENU_UPDATE:
            show_records()
            records = list_records()

            if not records:
                continue

            index = int(input(ENTER_UPDATE_INDEX_MESSAGE))
            new_record = create_record()

            if new_record is not None:
                if update_record(index, new_record):
                    print(RECORD_UPDATED_MESSAGE)
                else:
                    print(INVALID_INDEX_MESSAGE)

        elif option == MENU_DELETE:
            show_records()
            records = list_records()

            if not records:
                continue

            index = int(input(ENTER_DELETE_INDEX_MESSAGE))

            if delete_record(index):
                print(RECORD_DELETED_MESSAGE)
            else:
                print(INVALID_INDEX_MESSAGE)

        elif option == MENU_EXPORT:
            if export_records_to_csv():
                print(EXPORT_SUCCESS_MESSAGE)
            else:
                print(NO_DATA_TO_EXPORT_MESSAGE)

        elif option == MENU_RUN_R:
            output = run_r_script()
            print("\n=== R Script Output ===")
            print(output)

        elif option == MENU_RUN_WEATHER:
            output = run_weather_script()
            print(WEATHER_SCRIPT_OUTPUT_TITLE)
            print(output)

        elif option == MENU_EXIT:
            print(EXIT_MESSAGE)
            break

        else:
            print(INVALID_OPTION_MESSAGE)

if __name__ == "__main__":
    main()