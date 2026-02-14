from Data_Layer.StatCastDataLayer import *
from Constants.Events import *

def ClearData():
    ClearAndResetTables()

def AddData():
    AddNewStatcastdf()

def GetData(launch_angle, exit_velo, spray_angle, AngleForgiveness, VeloForgiveness, LaunchForgiveness):
    data = fetchData(launchAngle=launch_angle, exitVelocity=exit_velo, SprayAngle=spray_angle, 
                     AngleForgiveness=AngleForgiveness, VeloForgiveness=VeloForgiveness, LaunchForgiveness=LaunchForgiveness)
    if(data == []):
        return print('no data')
    AXBavg = 0
    AXSlg = 0
    # remove all sacrifice events
    for input in data:
        if(input[3] in Events.SACRIFICE):
            data.remove(input)
    print(data)
    entries = len(data)
    for input in data:
        if(input[3] in Events.BASE_HIT):
            AXBavg += 1
            match input[3]:
                case Events.SINGLE:
                    AXSlg += 1
                case Events.DOUBLE:
                    AXSlg += 2
                case Events.TRIPLE:
                    AXSlg += 3
                case Events.HOME_RUN:
                    AXSlg += 4
    AXBavg = float(AXBavg) / entries
    AXSlg = float(AXSlg) / entries
    print("Average: " + str(AXBavg) + "\nSlugging: " + str(AXSlg) + "\nSamples: "+ str(entries))
    return AXBavg, AXSlg, entries

