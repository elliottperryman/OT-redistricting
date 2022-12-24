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

class ShapeFileAlreadyDownloadedError(Exception):
    def __init__(self):
        super().__init__("State Shapefile already downloaded.")

class StateNumberDoesNotExistError(Exception):
    def __init__(self, nb):
        super().__init__(f"The given number ({nb}) does not represent a state.")
        self.number = nb

states_dict= { "ALABAMA": 1, "ALASKA": 2, "ARIZONA": 4, "ARKANSAS": 5, "CALIFORNIA": 6, "COLORADO": 8, "CONNECTICUT": 9, "DELAWARE": 10, "DISTRICT_OF_COLUMBIA": 11, "FLORIDA": 12, "GEORGIA": 13, "HAWAII": 15, "IDAHO": 16, "ILLINOIS": 17, "INDIANA": 18, "IOWA": 19, "KANSAS": 20, "KENTUCKY": 21, "LOUISIANA": 22, "MAINE": 23, "MARYLAND": 24, "MASSACHUSETTS": 25, "MICHIGAN": 26, "MINNESOTA": 27, "MISSISSIPPI": 28, "MISSOURI": 29, "MONTANA": 30, "NEBRASKA": 31, "NEVADA": 32, "NEW_HAMPSHIRE": 33, "NEW_JERSEY": 34, "NEW_MEXICO": 35, "NEW_YORK": 36, "NORTH_CAROLINA": 37, "NORTH_DAKOTA": 38, "OHIO": 39, "OKLAHOMA": 40, "OREGON": 41, "PENNSYLVANIA": 42, "RHODE_ISLAND": 44, "SOUTH_CAROLINA": 45, "SOUTH_DAKOTA": 46, "TENNESSEE": 47, "TEXAS": 48, "UTAH": 49, "VERMONT": 50, "VIRGINIA": 51, "WASHINGTON": 53, "WEST_VIRGINIA": 54, "WISCONSIN": 55, "WYOMING": 56, "PUERTO_RICO": 72}

def download_shapefile_bynumber(state_number):
    """
    Download US states shapefiles data from 
    https://www2.census.gov/geo/tiger/TIGER2020/TABBlOCK20/
    Download and unzip the file, removes unnecessary files only keeping the shapefile.
    """

    # tests whether the state_number exists
    if not state_number in states_dict.items:
        raise StateNumberDoesNotExistError(state_num)

    # Define the end directory where the the shapefile is extracted to
    fileName = f"tl_2020_{state_number:02d}_tabblock20.shp"
    datadir = f"{os.getcwd()}/data"

    # tests the existence of data directory
    if os.path.isdir(datadir):
        # tests if the file is already there
        if os.path.isfile(f"{datadir}/{fileName}"):
            raise ShapeFileAlreadyDownloadedError()
    else:
            os.mkdir(datadir)

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

        ## UNZIPPING THE FILE TO DATA FOLDER
        with zipfile.ZipFile(zipfile_path, "r") as file:
            file.extract(member=fileName, path=datadir)

def download_all_shapefiles():
    """
    Helper function to download all states shapefiles.
    """

    for state in states_dict:
        print(f"Downloading {state}...")
        try:
            download_shapefile_bynumber(states_dict[state])
        except ShapeFileAlreadyDownloadedError as e:
            print(str(e))
            continue
