from BatMath.backend.Business_Layer.StatCastBusinessLayer import AddData, ClearData, GetData
from BatMath.backend.Models.DxBA import DxBARequest


def clear_data():
    return ClearData()


def add_data():
    return AddData()


def calculate_dxba(request):
    return GetData(request)


def calculate_dxba_from_values(
    launch_angle,
    exit_velocity,
    spray_angle,
    angle_forgiveness,
    velocity_forgiveness,
    launch_forgiveness,
):
    request = DxBARequest(
        launch_angle=launch_angle,
        exit_velocity=exit_velocity,
        spray_angle=spray_angle,
        angle_forgiveness=angle_forgiveness,
        velocity_forgiveness=velocity_forgiveness,
        launch_forgiveness=launch_forgiveness,
    )
    return calculate_dxba(request)
