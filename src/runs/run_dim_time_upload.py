import sys, getopt, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from utils import basic
from db.dim_time_upload import DimTimeCreator

_DimTimeCreator = DimTimeCreator()
_DimTimeCreator.dim_time_upload()