import sys, getopt, os
import logging
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from utils import basic
from db.join_features import FeatureJoiner

feature_cols = ["c_fed_funds_rate.value",
                "c_ted_spread_credit_risk.value", #1986
                "c_usa_bond_2year.open", #1988
                "c_usa_bond_10year.open",
                "c_inflation_rate.value",
                "c_m2_growth.value",
                "c_sp500_bonds_return_ratio.value",
                "c_sp500_pe_ratio.value",
                "c_us_corporate_dept_to_gdp.value",
                "c_us_return_aaa_corporate_vs_bonds.value",
                "c_us_return_baa_corporate_vs_bonds.value",
                "c_bearmarket_days.value",
                "c_sp500.close"]

_FeatureJoiner = FeatureJoiner()
_FeatureJoiner.feature_join(feature_cols, "pre_features_20210521")