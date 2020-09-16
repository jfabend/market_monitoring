import sys, getopt, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from utils import basic
from db.join_features import FeatureJoiner

feature_cols = ["c_usa_bond_10year.open",
                "c_usa_bond_2year.open",
                "c_futures_sp500.hoch",
                "c_ted_spread_credit_risk.value",
                "c_leitzins_usa.value"]

_FeatureJoiner = FeatureJoiner()
_FeatureJoiner.feature_join(feature_cols, "basis_use_case")