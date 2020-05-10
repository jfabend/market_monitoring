import sys, getopt, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from utils import basic
from db.join_features import FeatureJoiner

feature_cols = ["c_futures_dax.erffn"]

_FeatureJoiner = FeatureJoiner()
_FeatureJoiner.feature_join(feature_cols)