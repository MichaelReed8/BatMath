import sqlite3
from datetime import date
from pathlib import Path
from pybaseball import statcast
from pybaseball.datahelpers.statcast_utils import add_spray_angle
from dateutil.relativedelta import relativedelta
import pandas as pd
from BatMath.backend.Models.DxBA import DataOperationResult


DB_PATH = Path(__file__).resolve().parents[2] / "BatMath.db"

CREATE_DXBA_TABLE_SQL = """
CREATE TABLE DxBA (
id INTEGER PRIMARY KEY,
spray_angle REAL NOT NULL,
event_outcome TEXT NOT NULL,
exit_velocity REAL NOT NULL,
launch_angle INTEGER NOT NULL,
CreateDate Text NOT NULL
);
"""


def get_connection():
    return sqlite3.connect(DB_PATH)


def ClearAndResetTables():
    connection = get_connection()
    cursor = connection.cursor()

    # Query to get all user-defined table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()

    # Drop each table
    for table_name in tables:
        # table_name is a tuple, so access the name via index [0]
        drop_query = f"DROP TABLE IF EXISTS {table_name[0]};"
        cursor.execute(drop_query)

    # Commit changes
    connection.commit()

    # recreate BatMath Table
    cursor.execute(CREATE_DXBA_TABLE_SQL)

    #Commit and Close
    connection.commit()
    connection.close()
    return DataOperationResult(
        success=True,
        message="DxBA table was cleared and recreated.",
        rows_affected=len(tables),
    )

def AddNewStatcastdf():
    connection = get_connection()
    cursor = connection.cursor()

    # try to get the most recent entry
    cursor.execute("SELECT CreateDate FROM DxBA ORDER BY CreateDate DESC LIMIT 1")

    row = cursor.fetchone()
    finalDate = date.today()
    if row is None or row[0] is None:
        currDate = '2008-01-01'
    else:
        currDate = row[0]
    currDate = date.fromisoformat(currDate)
    total_rows_added = 0

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
        total_rows_added += len(df_dxba)
        
        # Validation
        cursor.execute(
            "SELECT COUNT(*) FROM DxBA WHERE CreateDate = ?", 
            (today_str,)
        )
        entries = cursor.fetchone()[0]
        print(f"{entries} rows added")

    connection.close()
    return DataOperationResult(
        success=True,
        message="Statcast data import completed.",
        rows_affected=total_rows_added,
    )

def fetchData(launchAngle, exitVelocity, SprayAngle, AngleForgiveness, VeloForgiveness, LaunchForgiveness):
    #Calculate upper and lower ranges of exit velocity and spray angle
    connection = get_connection()
    cursor = connection.cursor()
    exitUpper = exitVelocity + VeloForgiveness
    exitLower = exitVelocity - VeloForgiveness
    AngleUpper = SprayAngle + AngleForgiveness
    AngleLower = SprayAngle - AngleForgiveness
    LaunchUpper = launchAngle + LaunchForgiveness
    LaunchLower = launchAngle - LaunchForgiveness
    query = (
        "Select spray_angle, exit_velocity, launch_angle, event_outcome "
        "From DxBA Where spray_angle <= ? and spray_angle >= ? "
        "and exit_velocity <= ? and exit_velocity >= ? "
        "and launch_angle <= ? and launch_angle >= ?"
    )
    cursor.execute(
        query,
        (
            AngleUpper,
            AngleLower,
            exitUpper,
            exitLower,
            round(LaunchUpper),
            round(LaunchLower),
        ),
    )
    results = cursor.fetchall()
    connection.close()
    return results
    
   


    
    
    
