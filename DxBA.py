from pybaseball import statcast
from pybaseball.datahelpers.statcast_utils import add_spray_angle
import pandas as pd
    

def calculateSprayExpectedBattingAverage( launchAngle, exitVelocity):
    
        data = statcast(start_dt='2023-01-01', end_dt='2024-12-31')
        data = data[~data["bb_type"].isna()]
        data = add_spray_angle(data)
        print("Spray angle ")
        print(data["spray_angle"][0:15])
        with open("dtypes_output.txt", "w") as f:
            f.write(data.dtypes.to_string())

    
        num_hits = data[data["events"].isin(["hit", "single", "double", "triple", "home_run"])]
              
        print(num_hits["events"][0:5])
        #print("Number of balls in dataset: ", num_balls)
    




