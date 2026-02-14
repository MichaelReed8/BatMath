from Business_Layer.StatCastBusinessLayer import *


def testing():
    while True:
        launch_angle = float(input('Please enter the launch angle:'))
        exit_velo = float(input('Please enter the exit velocity:'))
        spray_angle = float(input('Please enter the spray angle:'))
        range = float(input('please enter the range of forgiveness:'))
        print(GetData(launch_angle, exit_velo, spray_angle, range))


        