# unzip the files
import zipfile
# http request for the download
import requests
import os
import shutil
# creates tempdirectory for download and unzipping
import tempfile
# nice progress bars
from tqdm import tqdm

def download_state_number(state_number):
    """
    Download US states shapefiles data from 
    https://www2.census.gov/geo/tiger/TIGER2020/TABBlOCK20/
    Download and unzip the file, removes unnecessary files only keeping the shapefile.
    Corresponding state number :
        01_ALABAMA
        02_ALASKA
        04_ARIZONA
        05_ARKANSAS
        06_CALIFORNIA
        08_COLORADO
        09_CONNECTICUT
        10_DELAWARE
        11_DISTRICT_OF_COLUMBIA
        12_FLORIDA
        13_GEORGIA
        15_HAWAII
        16_IDAHO
        17_ILLINOIS
        18_INDIANA
        19_IOWA
        20_KANSAS
        21_KENTUCKY
        22_LOUISIANA
        23_MAINE
        24_MARYLAND
        25_MASSACHUSETTS
        26_MICHIGAN
        27_MINNESOTA
        28_MISSISSIPPI
        29_MISSOURI
        30_MONTANA
        31_NEBRASKA
        32_NEVADA
        33_NEW_HAMPSHIRE
        34_NEW_JERSEY
        35_NEW_MEXICO
        36_NEW_YORK
        37_NORTH_CAROLINA
        38_NORTH_DAKOTA
        39_OHIO
        40_OKLAHOMA
        41_OREGON
        42_PENNSYLVANIA
        44_RHODE_ISLAND
        45_SOUTH_CAROLINA
        46_SOUTH_DAKOTA
        47_TENNESSEE
        48_TEXAS
        49_UTAH
        50_VERMONT
        51_VIRGINIA
        53_WASHINGTON
        54_WEST_VIRGINIA
        55_WISCONSIN
        56_WYOMING
        72_PUERTO_RICO
    """

    # Opens a tempdir to download the file and unzip it
    with tempfile.TemporaryDirectory() as dirpath:
        ## DOWNLOADING THE ZIP ARCHIVE
        # big files so setting stream to true to keep connection active
        http_response = requests.get(f"https://www2.census.gov/geo/tiger/TIGER2020/TABBlOCK20/tl_2020_{state_number:02d}_tabblock20.zip", stream=True)
        file_size = int(http_response.headers.get('content-length'))

        # Open as binary to write the chunks in
        with open(f"{dirpath}/tl_2020_{state_number:02d}_tabblock.zip", "wb") as zip_archive, tqdm(total=file_size, unit='iB', unit_scale=True, unit_divisor=1024, desc="Downloading zipfile", colour="green") as pbar :
            for chunk in http_response.iter_content(chunk_size=1024):
                if chunk:
                    zip_archive.write(chunk)
                    pbar.update(len(data))

        ## UNZIPPING THE ARCHIVE
        with zipfile.ZipFile(f"{dirpath}/tl_2020_{state_number:02d}_tabblock.zip", "r") as zip_archive:
            zip_archive.extractall(path=dirpath)

        end_directory = f"{os.getcwd()}/data"
        start_fileName = f"{dirpath}/tl_2020_{state_number:02d}_tabblock20.shp"
        end_fileName = f"{os.getcwd()}/data/tl_2020_{state_number:02d}_tabblock20.shp"
        ## MOVING THE SHAPEFILE TO DATA/
        # tests the existence of data directory
        if not os.path.isdir():
            os.mkdir(f"{os.getcwd()}/data")

        with open(end_fileName, 'wb') as end_file:
            with open(start_fileName, 'rb') as start_file:
                shutil.copyfileobj(end_file, start_file)

#TODO : implement tqdm wrapattr for a nice progress bar
