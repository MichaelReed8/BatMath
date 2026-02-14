from Business_Layer.StatCastBusinessLayer import *


def testing():
    while True:
        launch_angle = float(input('Please enter the launch angle:'))
        exit_velo = float(input('Please enter the exit velocity:'))
        spray_angle = float(input('Please enter the spray angle:'))
        AngleForgiveness = float(input('please enter the range of Spray Angle Forgiveness:'))
        VeloForgiveness = float(input('Please enter the range of Velocity Forgiveness:'))
        LaunchForgiveness = float(input('Please enter the range of Launch Angle Forgiveness:'))
        print(GetData(launch_angle, exit_velo, spray_angle, AngleForgiveness, VeloForgiveness, LaunchForgiveness))


        