from area_calculations import (
    calculate_rectangular_area,
    calculate_grape_row_count,
    calculate_total_row_length,
    calculate_grape_area
)
from input_calculations import (
    calculate_grape_input,
    calculate_corn_input
)
from constants import (
    GRAPE,
    CORN,
    ENTER_CROP_TYPE_MESSAGE,
    ENTER_WIDTH_MESSAGE,
    ENTER_LENGTH_MESSAGE,
    ENTER_INPUT_TYPE_MESSAGE,
    ENTER_ROW_SPACING_MESSAGE,
    ENTER_GRAPE_INPUT_DOSAGE_MESSAGE,
    ENTER_CORN_INPUT_DOSAGE_MESSAGE,
    INVALID_CROP_TYPE_MESSAGE,
    INVALID_NUMBER_MESSAGE,
    INVALID_POSITIVE_NUMBER_MESSAGE,
    INVALID_TEXT_MESSAGE,
    INVALID_ROW_SPACING_MESSAGE
)

def get_valid_text(message):
    while True:
        value = input(message).strip().lower()

        if value and any(character.isalpha() for character in value):
            return value

        print(INVALID_TEXT_MESSAGE)

def get_valid_crop_type():
    while True:
        crop_type = input(ENTER_CROP_TYPE_MESSAGE).strip().lower()

        if crop_type == GRAPE or crop_type == CORN:
            return crop_type

        print(INVALID_CROP_TYPE_MESSAGE)

def get_positive_float(message):
    while True:
        value = input(message).strip()

        try:
            value = float(value)

            if value > 0:
                return value

            print(INVALID_POSITIVE_NUMBER_MESSAGE)

        except ValueError:
            print(INVALID_NUMBER_MESSAGE)

def create_record():
    crop_type = get_valid_crop_type()
    width_meters = get_positive_float(ENTER_WIDTH_MESSAGE)
    length_meters = get_positive_float(ENTER_LENGTH_MESSAGE)
    input_type = get_valid_text(ENTER_INPUT_TYPE_MESSAGE)

    if crop_type == GRAPE:
        input_dosage = get_positive_float(ENTER_GRAPE_INPUT_DOSAGE_MESSAGE)

        while True:
            row_spacing_meters = get_positive_float(ENTER_ROW_SPACING_MESSAGE)

            if row_spacing_meters <= width_meters:
                break

            print(INVALID_ROW_SPACING_MESSAGE)

        area = calculate_grape_area(width_meters, length_meters)
        row_count = calculate_grape_row_count(width_meters, row_spacing_meters)
        total_row_length = calculate_total_row_length(row_count, length_meters)
        total_input = calculate_grape_input(total_row_length, input_dosage)

        record = [
            crop_type,
            width_meters,
            length_meters,
            area,
            input_type,
            input_dosage,
            total_input,
            row_spacing_meters,
            row_count,
            total_row_length
        ]

        return record

    input_dosage = get_positive_float(ENTER_CORN_INPUT_DOSAGE_MESSAGE)

    area = calculate_rectangular_area(width_meters, length_meters)
    total_input = calculate_corn_input(area, input_dosage)

    record = [
        crop_type,
        width_meters,
        length_meters,
        area,
        input_type,
        input_dosage,
        total_input,
        None,
        None,
        None
    ]

    return record