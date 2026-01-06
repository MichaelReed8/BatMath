from DxBA import calculateSprayExpectedBattingAverage
from pybaseball import cache
cache.enable()
#print('hi')
launchAngle = 15
exitVelocity = 95.0
calculateSprayExpectedBattingAverage(launchAngle, exitVelocity)