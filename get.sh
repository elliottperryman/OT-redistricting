#!/bin/bash
mkdir -p data
num=47
cd data && wget https://www2.census.gov/geo/tiger/TIGER2020/TABBLOCK20/tl_2020_${num}_tabblock20.zip && unzip tl_2020_${num}_tabblock20.zip

