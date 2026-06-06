from BatMath.backend.Constants.Events import Events
from BatMath.backend.Data_Layer.StatCastDataLayer import (
    AddNewStatcastdf,
    ClearAndResetTables,
    fetchData,
)
from BatMath.backend.Models.DxBA import DxBARequest, DxBAResult

def ClearData():
    return ClearAndResetTables()

def AddData():
    return AddNewStatcastdf()

def GetData(request: DxBARequest):
    data = fetchData(
        launchAngle=request.launch_angle,
        exitVelocity=request.exit_velocity,
        SprayAngle=request.spray_angle,
        AngleForgiveness=request.angle_forgiveness,
        VeloForgiveness=request.velocity_forgiveness,
        LaunchForgiveness=request.launch_forgiveness,
    )

    data = [batted_ball for batted_ball in data if batted_ball[3] not in Events.SACRIFICE]
    entries = len(data)

    if entries == 0:
        return DxBAResult(batting_average=0.0, slugging=0.0, samples=0)

    hits = 0
    total_bases = 0
    for batted_ball in data:
        event_outcome = batted_ball[3]
        if event_outcome in Events.BASE_HIT:
            hits += 1
            match event_outcome:
                case Events.SINGLE:
                    total_bases += 1
                case Events.DOUBLE:
                    total_bases += 2
                case Events.TRIPLE:
                    total_bases += 3
                case Events.HOME_RUN:
                    total_bases += 4

    return DxBAResult(
        batting_average=float(hits) / entries,
        slugging=float(total_bases) / entries,
        samples=entries,
    )

