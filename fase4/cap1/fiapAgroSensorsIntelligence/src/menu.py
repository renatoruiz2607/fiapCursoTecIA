from sensor_data_service import (
    show_current_sensor_data,
    show_productivity_index,
    show_agricultural_recommendation,
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

        elif option == "0":
            print("\nEncerrando o sistema...")
            break

        else:
            print("\nOpção inválida.")

        input("\nPressione ENTER para continuar...")