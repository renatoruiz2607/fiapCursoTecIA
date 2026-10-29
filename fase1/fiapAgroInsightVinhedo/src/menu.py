from constants import (
    MENU_TITLE,
    MENU_ADD_TEXT,
    MENU_LIST_TEXT,
    MENU_UPDATE_TEXT,
    MENU_DELETE_TEXT,
    MENU_EXPORT_TEXT,
    MENU_RUN_R_TEXT,
    MENU_RUN_WEATHER_TEXT,
    MENU_EXIT_TEXT,
    MENU_CHOOSE_OPTION_TEXT
)

def display_menu():
    print(MENU_TITLE)
    print(MENU_ADD_TEXT)
    print(MENU_LIST_TEXT)
    print(MENU_UPDATE_TEXT)
    print(MENU_DELETE_TEXT)
    print(MENU_EXPORT_TEXT)
    print(MENU_RUN_R_TEXT)
    print(MENU_RUN_WEATHER_TEXT)
    print(MENU_EXIT_TEXT)

def get_menu_option():
    display_menu()
    option = input(MENU_CHOOSE_OPTION_TEXT).strip()
    return option