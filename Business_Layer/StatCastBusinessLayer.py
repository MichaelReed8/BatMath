from Data_Layer.StatCastDataLayer import *

def ClearData():
    ClearAndResetTables()

def AddData():
    AddNewStatcastdf()

def GetData():
    return fetchData(23, 94.5, 24.5, 0.5)