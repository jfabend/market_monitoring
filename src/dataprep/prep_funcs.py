import pandas as pd
import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

from sklearn.preprocessing import StandardScaler

from utils import basic
from db.get_dbtable_data import get_dbtable_data

def drop_na_rows(df):
    for col in df.columns:
        df = df[~pd.isnull(df[col])]
    return df
    
def mean_by_group(df, targetcol, groupcols):
    return df.groupby(groupcols)[targetcol].mean()

def new_col_substract(df, base_col, sub_col, new_col):
    df[new_col] = df[base_col] - df[sub_col]
    return df

def new_col_percent_delta(df, base_col, new_col, days):
    """Percentage of decrease / increase of base col compared to minus x days 

    Args:
        df (dataFrame): the dataframe
        base_col (str): the regarded numeric column
        new_col (str): name of the new column
        days (int): which day in the past shall be used for comparison

    Returns:
        [type]: [description]
    """
    df[new_col] = (df[base_col] / df[base_col].shift(days)) * 100 - 100
    return df

def shift_col_preview(df, base_col, new_col, days):
    """add the value of base col x days in the future to the current row

    Args:
        df (dataFrame): the dataframe
        base_col (str): the column to be shifted
        new_col (str): name of the new column
        days (int): which day in the future shall be added to the current rows

    Returns:
        [type]: [description]
    """
    df[new_col] = df[base_col].shift(-days)
    return df

def rolling_mean(df, base_col, new_col, days):
    df[new_col] = df[base_col].rolling(days).mean() 
    return df

def remove_by_value(df, base_col, value):
    df = df[df[base_col] != value]
    return df

def standardscaling(df, cols):
    scaler = StandardScaler().fit(df[cols])
    X_train_scaled = scaler.transform(df[cols])
    return X_train_scaled