import sqlite3
from datetime import date
from pybaseball import statcast
from pybaseball.datahelpers.statcast_utils import add_spray_angle
from dateutil.relativedelta import relativedelta
import pandas as pd


def ClearAndResetTables():
    connection = sqlite3.connect('BatMath.db')
    cursor = connection.cursor()

    # Query to get all user-defined table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()

    # Drop each table
    for table_name in tables:
        # table_name is a tuple, so access the name via index [0]
        drop_query = f"DROP TABLE IF EXISTS {table_name[0]};"
        print(f"Executing: {drop_query}")
        cursor.execute(drop_query)

    # Commit changes
    connection.commit()

    # recreate BatMath Table
    cursor.execute("""
    CREATE TABLE DxBA (
    id INTEGER PRIMARY KEY,
    spray_angle REAL NOT NULL,
    event_outcome TEXT NOT NULL,
    exit_velocity REAL NOT NULL,
    launch_angle INTEGER NOT NULL,
    CreateDate Text NOT NULL             
    );
    
    """)

    #Commit and Close
    connection.commit()
    connection.close()

def AddNewStatcastdf():
    connection = sqlite3.connect('BatMath.db')
    cursor = connection.cursor()

    # try to get the most recent entry
    cursor.execute("SELECT CreateDate FROM DxBA ORDER BY CreateDate LIMIT 1")

    currDate = cursor.fetchone()[0]
    finalDate = date.today()
    if currDate is None:
        currDate = '2008-01-01'
    currDate = date.fromisoformat(currDate)
    while currDate < finalDate: 
        #fetch all statcast df from after this day
        endDate = currDate + relativedelta(years=1)
        print(endDate)
        df = statcast(start_dt=currDate.isoformat(), end_dt=endDate.isoformat())
        currDate = currDate + relativedelta(years=1)
        #trim off all pitches that do not result in a bb_type
        df = df[~df["bb_type"].isna()]
        df = add_spray_angle(df, adjusted=False)
        # create a new object with only the information we need

        column_map = {
        "spray_angle": "spray_angle",
        "events": "event_outcome",
        "launch_speed": "exit_velocity",
        "launch_angle": "launch_angle"
        }

        # today's date (YYYY-MM-DD)
        today_str = finalDate.isoformat()

        df_dxba = (
        df
        .loc[:, df.columns.intersection(column_map.keys())]
        .rename(columns=column_map)
        .dropna(subset=["exit_velocity", "launch_angle", "spray_angle"])
        .assign(CreateDate=today_str)
        .reset_index(drop=True)
        )

        #ensure data is formatted correctly
        df_dxba = df_dxba.astype({
        "spray_angle": "float",
        "exit_velocity": "float",
        "launch_angle": "int",
        "event_outcome": "string",
        "CreateDate": "string"
        })

        #insert into the database
        df_dxba.to_sql(
            "DxBA",
            connection,
            if_exists="append",
            index=False
        )
        
        # Validation
        cursor.execute(
            "SELECT COUNT(*) FROM DxBA WHERE CreateDate = ?", 
            (today_str,)
        )
        entries = cursor.fetchone()[0]
        print(f"{entries} rows added")

def fetchData(launchAngle, exitVelocity, SprayAngle, AngleForgiveness, VeloForgiveness, LaunchForgiveness):
    #Calculate upper and lower ranges of exit velocity and spray angle
    connection = sqlite3.connect('BatMath.db')
    cursor = connection.cursor()
    exitUpper = exitVelocity + VeloForgiveness
    exitLower = exitVelocity - VeloForgiveness
    AngleUpper = SprayAngle + AngleForgiveness
    AngleLower = SprayAngle - AngleForgiveness
    LaunchUpper = launchAngle + LaunchForgiveness
    LaunchLower = launchAngle - LaunchForgiveness
    query = (f"Select spray_angle, exit_velocity, launch_angle, event_outcome "
             f"From DxBA Where spray_angle <= {AngleUpper} and spray_angle >= {AngleLower} "
            f"and exit_velocity <= {exitUpper} and exit_velocity >= {exitLower} "
             f"and launch_angle <= {round(LaunchUpper)} and launch_angle >= {round(LaunchLower)}" )
    cursor.execute(query)
    return cursor.fetchall()
    
   


    
    
    