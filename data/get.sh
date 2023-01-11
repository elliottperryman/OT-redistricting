for i in {10..78}; do wget https://www2.census.gov/geo/tiger/TIGER2020/TABBLOCK20/tl_2020_${i}_tabblock20.zip; done;
for i in {1..9}; do wget https://www2.census.gov/geo/tiger/TIGER2020/TABBLOCK20/tl_2020_0${i}_tabblock20.zip; done;
for i in *.zip; do unzip $i; done;
rm *.zip

