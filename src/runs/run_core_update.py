import sys, getopt, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from utils import basic
from db.core_update import CoreUpdate

_CoreUpdate = CoreUpdate()
_CoreUpdate.core_update()