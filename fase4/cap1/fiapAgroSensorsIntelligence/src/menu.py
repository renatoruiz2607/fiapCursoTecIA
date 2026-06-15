from sensor_data_service import (
    show_current_sensor_data,
    show_productivity_index,
    show_agricultural_recommendation,
    save_current_sensor_data,
)

from services.ingestion_service import (
    start_automatic_ingestion,
    stop_automatic_ingestion,
    show_ingestion_status,
)


def show_header():
    print("\n======================================")
    print(" AGRO SENSORS INTELLIGENCE")
    print("======================================")


def show_menu():
    print("\nMenu principal:")
    print("1 - Exibir leitura atual dos sensores")
    print("2 - Exibir produtividade esperada")
    print("3 - Exibir recomendação agrícola")
    print("4 - Salvar leitura atual no banco de dados")
    print("5 - Iniciar ingestão automática")
    print("6 - Exibir status da ingestão")
    print("7 - Parar ingestão automática")
    print("0 - Sair")


def start_menu():
    while True:
        show_header()
        show_menu()

        option = input("\nSelecione uma opção: ").strip()

        if option == "1":
            show_current_sensor_data()

        elif option == "2":
            show_productivity_index()

        elif option == "3":
            show_agricultural_recommendation()

        elif option == "4":
            save_current_sensor_data()

        elif option == "5":
            start_automatic_ingestion(interval_seconds=10)

        elif option == "6":
            show_ingestion_status()

        elif option == "7":
            stop_automatic_ingestion()

        elif option == "0":
            stop_automatic_ingestion()
            print("\nEncerrando o sistema...")
            break

        else:
            print("\nOpção inválida.")

        input("\nPressione ENTER para continuar...")