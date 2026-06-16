import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from database.database import initialize_database
from menu import start_menu


def main():
    initialize_database()
    start_menu()


if __name__ == "__main__":
    main()