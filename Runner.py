from DxBA import calculateSprayExpectedBattingAverage
from pybaseball import cache
from Business_Layer.StatCastBusinessLayer import *
cache.enable()
#print('hi')
launchAngle = 15
exitVelocity = 95.0
# calculateSprayExpectedBattingAverage(launchAngle, exitVelocity)
AddData()
res = GetData()
print(res)
