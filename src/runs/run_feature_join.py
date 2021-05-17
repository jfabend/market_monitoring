import sys, getopt, os
import logging
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from utils import basic
from db.join_features import FeatureJoiner

feature_cols = ["c_capacity_utilization.value",
                "c_industrial_production.value",
                "c_fed_funds_rate.value",
                "c_us_national_unemployment_rate.value",
                #"c_ted_spread_credit_risk.value",
                #"c_vix.close",
                #"c_usa_bond_2year.open",
                #"c_usa_bond_10year.open",
                #"c_sugar_prices.value",
                "c_sp500.close"]

_FeatureJoiner = FeatureJoiner()
_FeatureJoiner.feature_join(feature_cols, "pre_features_20210516")