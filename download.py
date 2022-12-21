# unzip the files
import zipfile
# http request for the download
import requests
# get the currend working directory
import os
# creates a temp directory for the download
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
        http_response = requests.get(f"https://www2.census.gov/geo/tiger/TIGER2020/TABBLOCK20/tl_2020_{state_number:02d}_tabblock20.zip", stream=True)
        zipfile_size = int(http_response.headers['content-length'])

        zipfile_path = f"{dirpath}/tl_2020_{state_number:02d}_tabblock.zip"

        # Open as binary to write the chunks in
        with open(zipfile_path, "wb") as file, tqdm(total=zipfile_size, unit='iB', unit_scale=True, unit_divisor=1024, desc="Downloading Zipfile", colour="green") as pbar :
            for chunk in http_response.iter_content(chunk_size=1024):
                file.write(chunk)
                pbar.update(len(chunk))

        # Define the end directory where the the shapefile is extracted to
        fileName = f"tl_2020_{state_number:02d}_tabblock20.shp"
        datadir = f"{os.getcwd()}/data"

        # tests the existence of data directory
        if not os.path.isdir(datadir):
            os.mkdir(datadir)

        ## UNZIPPING THE FILE TO DATA FOLDER
        with zipfile.ZipFile(zipfile_path, "r") as file:
            file.extract(member=fileName, path=datadir)
