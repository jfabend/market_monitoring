import sys, getopt, os
import logging
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from utils import basic
from db.join_features import FeatureJoiner

feature_cols = ["c_usa_bond_10year.open",
                "c_usa_bond_2year.open",
                "c_vix.high",
                #"c_ted_spread_credit_risk.value",
                "c_leitzins_usa.value",
                "c_sp500.volume",
                "c_sp500.high"]

_FeatureJoiner = FeatureJoiner()
_FeatureJoiner.feature_join(feature_cols, "basis_use_case_zwei")