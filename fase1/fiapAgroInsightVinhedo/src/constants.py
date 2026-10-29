# Menu options
MENU_ADD = "1"
MENU_LIST = "2"
MENU_UPDATE = "3"
MENU_DELETE = "4"
MENU_EXPORT = "5"
MENU_RUN_R = "6"
MENU_RUN_WEATHER = "7"
MENU_EXIT = "0"

# Crop types
GRAPE = "grape"
CORN = "corn"

# Record indexes
INDEX_CROP_TYPE = 0
INDEX_WIDTH_METERS = 1
INDEX_LENGTH_METERS = 2
INDEX_AREA = 3
INDEX_INPUT_TYPE = 4
INDEX_INPUT_DOSAGE = 5
INDEX_TOTAL_INPUT = 6
INDEX_ROW_SPACING_METERS = 7
INDEX_ROW_COUNT = 8
INDEX_TOTAL_ROW_LENGTH = 9

# Messages
INVALID_OPTION_MESSAGE = "Invalid option. Please try again."
EMPTY_RECORDS_MESSAGE = "No records found."
INVALID_INDEX_MESSAGE = "Invalid index."
RECORD_ADDED_MESSAGE = "Record added successfully."
RECORD_UPDATED_MESSAGE = "Record updated successfully."
RECORD_DELETED_MESSAGE = "Record deleted successfully."
EXIT_MESSAGE = "Program finished."
INVALID_CROP_TYPE_MESSAGE = "Invalid crop type. Please enter grape or corn."
INVALID_NUMBER_MESSAGE = "Invalid value. Please enter a numeric value."
INVALID_POSITIVE_NUMBER_MESSAGE = "Invalid value. Please enter a number greater than zero."
INVALID_ROW_SPACING_MESSAGE = "Row spacing cannot be greater than field width."
INVALID_TEXT_MESSAGE = "Invalid value. Please enter text."
EXPORT_SUCCESS_MESSAGE = "Data exported successfully to CSV."
EXPORT_ERROR_MESSAGE = "An error occurred while exporting data."
NO_DATA_TO_EXPORT_MESSAGE = "There are no records to export."

# Input prompts
ENTER_CROP_TYPE_MESSAGE = "Enter crop type (grape/corn): "
ENTER_WIDTH_MESSAGE = "Enter field width in meters: "
ENTER_LENGTH_MESSAGE = "Enter field length in meters: "
ENTER_INPUT_TYPE_MESSAGE = "Enter input type: "
ENTER_GRAPE_INPUT_DOSAGE_MESSAGE = "Enter input dosage per linear meter: "
ENTER_CORN_INPUT_DOSAGE_MESSAGE = "Enter input dosage per square meter: "
ENTER_ROW_SPACING_MESSAGE = "Enter row spacing in meters: "
ENTER_UPDATE_INDEX_MESSAGE = "Enter the record index to update: "
ENTER_DELETE_INDEX_MESSAGE = "Enter the record index to delete: "
R_SCRIPT_SUCCESS_MESSAGE = "R script executed successfully."
R_SCRIPT_ERROR_MESSAGE = "Error running R script."
WEATHER_SCRIPT_ERROR_MESSAGE = "Error running weather report script."

# Menu texts
MENU_TITLE = "\n=== Agro Insight Vinhedo Menu ==="
MENU_ADD_TEXT = "1 - Add record"
MENU_LIST_TEXT = "2 - List records"
MENU_UPDATE_TEXT = "3 - Update record"
MENU_DELETE_TEXT = "4 - Delete record"
MENU_EXPORT_TEXT = "5 - Export records to CSV"
MENU_RUN_R_TEXT = "6 - Run statistical analysis (R)"
MENU_RUN_WEATHER_TEXT = "7 - Run weather report (R)"
WEATHER_SCRIPT_OUTPUT_TITLE = "\n=== Weather Report ==="
MENU_EXIT_TEXT = "0 - Exit"
MENU_CHOOSE_OPTION_TEXT = "Choose an option: "

# CSV path
CSV_FILE_PATH = "data/agricultural_data.csv"

# R scripts paths
R_SCRIPT_PATH = "scripts/agricultural_statistics.R"
WEATHER_SCRIPT_PATH = "scripts/weather_report.R"