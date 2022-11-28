from dbfread import DBF
rec = DBF('data/tl_2020_10_tabblock20.dbf')
red
rec
rec[0]
for r in rec:
    print(r)
from pandas import DataFrame
df = DataFrame(iter(rec))
df.head()
df.shape
ls data/*
ls data/_26_*
ls data/*_26_*
import fiona
!git push
c =  fiona.open('data/tl_2020_10_tabblock20.shp', 'r')
c
c
c.meta
c['schema']
c.meta
c.keys()
list(_)
c[0]
c[0]['properties']
c[0]['geometry']
c[0]['geometry']
c.close()
%history -n 30
%history



import numpy as np
import fiona
!cat notes.py
from dbfread import DBF
c = fiona.open('data/tl_2020_10_tabblock20.shp', 'r')
c[0]
from shapely import shape
from shapely.geometry import shape
shape(c[0]['geometry'])
p = -
shape(c[0]['geometry'])
p = _
p
p.centroid?
p.centroid
p.centroid.x
p.centroid.y
c[0]['properties'][:4]
c[0]['properties']
c[0]['properties'][0]
c[0]['properties']['STATEFP20']
len(c)
len(c)**2
len([_ for _ in c if _['properties']['POP20']>0])
_**2
len([_ for _ in c if _['properties']['POP20']>1])
len([_ for _ in c if _['properties']['POP20']>0])
len([_ for _ in c if _['properties']['POP20']>10])
len([_ for _ in c if _['properties']['POP20']>100])
len([_ for _ in c if _['properties']['POP20']>1000])
import pandas as pd
pd.DataFrame([{'POP20':_['properties']['POP20']} for _ in c])
%history
