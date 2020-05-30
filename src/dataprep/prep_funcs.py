import pandas as pd
import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

from utils import basic
from db.get_dbtable_data import get_dbtable_data

def drop_na_rows(df):
    for col in df.columns:
        df = df[~pd.isnull(df[col])]
    return df
    
def mean_by_group(df, targetcol, groupcols):
    return df.groupby(groupcols)[targetcol].mean()

