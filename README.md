# OT-redistricting

This is an implementation of redistricting using Optimal Transport.

## How to use:

source start.sh or install the environment manually with requirements.txt.

## where is this data stored?

The data currently used comes from TIGER2020 a project of the US Census Bureau.
You can learn more about it [here][https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.2020.html#list-tab-JMJDQEOVO9RD9R31BU]

## How to plot data:

    with a GeoDataFrame:
     This one works !!!
     `df.plot(column=df.index.values, categorical=True, legend=True)`
        * df.plot(column='district', categorical=True, legend=True)
        * df.plot(column=districts, categorical=True, legend=True)

## Known Bugs:

 * I forgot to make the centroids weighted by population
 * The earth is not flat
    * figure out how to convert to flat earth
    * figure out the right projections (seems hard as projection depends on location)
 * I think I should start the centroids by sampling from population(X)
 * the centers should be plotted as well
 * the iterative algorithm doesn't work because of the -1 districts
