from BatMath.backend.Controller_Layer.StatcastControllerLayer import (
    add_data,
    calculate_dxba_from_values,
    clear_data,
)


def prompt_for_float(prompt):
    return float(input(prompt))


def print_menu():
    print("")
    print("Select a controller endpoint:")
    print("1. Calculate DxBA")
    print("2. Clear and reset data")
    print("3. Add new Statcast data")
    print("4. Exit")


def run_dxba_prompt():
    launch_angle = prompt_for_float("Please enter the launch angle: ")
    exit_velocity = prompt_for_float("Please enter the exit velocity: ")
    spray_angle = prompt_for_float("Please enter the spray angle: ")
    angle_forgiveness = prompt_for_float("Please enter the range of spray angle forgiveness: ")
    velocity_forgiveness = prompt_for_float("Please enter the range of velocity forgiveness: ")
    launch_forgiveness = prompt_for_float("Please enter the range of launch angle forgiveness: ")

    result = calculate_dxba_from_values(
        launch_angle=launch_angle,
        exit_velocity=exit_velocity,
        spray_angle=spray_angle,
        angle_forgiveness=angle_forgiveness,
        velocity_forgiveness=velocity_forgiveness,
        launch_forgiveness=launch_forgiveness,
    )

    print(f"Average: {result.batting_average}")
    print(f"Slugging: {result.slugging}")
    print(f"Samples: {result.samples}")


def print_data_operation_result(result):
    print(result.message)
    print(f"Rows affected: {result.rows_affected}")


def run_cli():
    while True:
        print_menu()
        selected_endpoint = input("Endpoint: ").strip()

        if selected_endpoint == "1":
            run_dxba_prompt()
        elif selected_endpoint == "2":
            result = clear_data()
            print_data_operation_result(result)
        elif selected_endpoint == "3":
            result = add_data()
            print_data_operation_result(result)
        elif selected_endpoint == "4":
            break
        else:
            print("Unknown endpoint.")


if __name__ == "__main__":
    run_cli()
