import pandas as pd
import numpy as np
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

def shift_cols_preview(df, cols, days):
    """add the value of base col x days in the future to the current row

    Args:
        df (dataFrame): the dataframe
        cols (str): the columns to be shifted
        days (int): which day in the future shall be added to the current rows

    Returns:
        [type]: [description]
    """
    for col in cols:
        new_col_name = col + "_shiftprev_" + str(days)
        df[new_col_name] = df[col].shift(-days)
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

def less_greater_encoding(df, base_col, new_col, threshold):
    def func(row):
        if row[base_col] >= threshold:
            return 1
        else:
            return 0

    df[new_col] = df.apply(func, axis=1)
    return df

def two_cols_percent_delta(df, base_col, second_col, new_col):
    df[new_col] = (df[second_col] / df[base_col]) * 100 - 100
    return df

def keep_dtype_only(df, base_col, dtype):
    def type_check(x):
        return type(x) is eval(dtype)

    df = df[df[base_col].apply(lambda x: type_check(x))]
    return df

def set_col_dtype(df, base_col, dtype):
    df[base_col] = df[base_col].astype(dtype)
    return df