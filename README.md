# OT-redistricting

This is an implementation of redistricting using Optimal Transport.

## How to use:

source start.sh or install the environment manually with requirements.txt.

## What data is used? / What happened to data?

 * The data currently used comes from TIGER2020 a project of the US Census Bureau.
You can learn more about it [here](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.2020.html#list-tab-JMJDQEOVO9RD9R31BU) and download [here](https://www2.census.gov/geo/tiger/TIGER2020/TABBLOCK20/)
 * I think we should move to downloaded data. It removes wifi problems and all the associated problems

## To Do list:
 * projections. I think that .to_crs(crs=3857).centroid.to_crs(4269) should workarino
 * right now all districts are being called as split. this is wrong.
 * semidiscrete case
 * report
 * check if rounded and split solution has lower cost
 * the random guesses should be drawn from a poisson point process with intensity equal to the population
 * the population weighting should just sum
