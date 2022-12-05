# OT-redistricting

## How to use:
 * start vpn
 * ssh to username@ensipc175.ensimag.fr
 * cd /scratch/OT\_redistricting/
 * source start.sh (all packages installed into anaconda base) 

## How to start an ensipc computer
send email to "ensipc-wake" <ensipc-wake@ensimag.fr>
with content: ensipc175

## where is this data stored?
ensipc333 at /scratch/OT\_redistricting

## How to get vpn connected:
host: vpn-etu.ensimag.fr
username and password same as school username and password

## How the data is fetched:
data/get.sh

## How to plot data:
    with a GeoDataFrame:
        * df.plot(column=df.index.values, categorical=True, legend=True)
        * df.plot(column='district', categorical=True, legend=True)
        * df.plot(column=districts, categorical=True, legend=True)

## Known Bugs:
 * I forgot to make the centroids weighted by population
 * The earth is not flat
    * figure out how to convert to flat earth
    * figure out the right projections (seems hard as projection depends on location)
 * I think I should start the centroids by sampling from population(X)
