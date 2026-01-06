**NOTE**: This is a WIP

BatMath is a WIP Repository with the objective to create new statistics in baseball. This is done by pulling statcast information using the pybaseball library.

## Problem Statement

I love baseball, and I love all the stats that are included in it. One thing struck me as odd in the world of advanced statistics. For the most part, it seems that people believe that once a ball is put into play, you have no control over direction. I believe this does not correctly reward players that are able to hit the ball where the defense isn't, as opposed to the current standard of removing defense from the equation. therefore, I want to build statistics that can show how hitting the ball in a particular direction can reward players substantially.

## Current Iteration Plan ##

1. Build Db functions to pull statcast data to a local SQLite Implementation.

2. Create **Adjusted expected Batting Average (AdxBA)**, A statistic that determines the probability of a Batted Ball being a hit, based on launch angle, velocity, and spray angle.<br>
Based on expected Batting Average (xBA), where xBA does not include spray angle (direction of batted ball) into its calculation

3. Create a simple webpage to query this data and return a result


## Future Plans

1. More Statistics:
     * Adjusted expected slugging percentage (AdxSLG), which would measure the expected slugging percentage of a batted ball **inclusive** of spray angle
     * A Gap Shot (GS) is a theoretical boolean statistic I am terming that would determine whether a batted ball is put into a gap. to determine this, you would compare the adxBA to the xBA. if the adxBA is significantly higher then the xBA, it implies that the batter hit the ball where the defender is not. This statistic would only apply to balls hit to the outfield, shifting in the infield is much more aggressive than the outfield
