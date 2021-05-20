import pandas as pd
import numpy as np
import sys, os
import math
from dotenv import load_dotenv
import box
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

from utils import basic
from db.get_dbtable_data import get_dbtable_data

def drop_na_rows(df, special_col=""):
    if special_col == "":
        for col in df.columns:
            df = df[~pd.isnull(df[col])]
    else:
        df = df[~pd.isnull(df[special_col])]
    return df
    
def mean_by_group(df, targetcol, groupcols):
    return df.groupby(groupcols)[targetcol].mean()

def new_col_substract(df, base_col, sub_col, new_col):
    df[new_col] = df[base_col] - df[sub_col]
    return df

def col_past_percent_delta(df, cols, days):
    """Percentage of decrease / increase of a column compared to minus x days 

    Args:
        df (dataFrame): the dataframe
        base_col (str): the regarded numeric column
        new_col (str): name of the new column
        days (int): which day in the past shall be used for comparison

    Returns:
        [type]: [description]
    """
    if type(cols) == box.box_list.BoxList:
        for col in cols:
            new_col_name = col + "_changeperc_" + str(days)
            df[new_col_name] = (df[col] / df[col].shift(days)) * 100 - 100
    if type(cols) == str:
        new_col_name = cols + "_changeperc_" + str(days)
        df[new_col_name] = (df[cols] / df[cols].shift(days)) * 100 - 100
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
    if type(cols) == box.box_list.BoxList:
        for col in cols:
            new_col_name = col + "_shiftprev_" + str(days)
            df[new_col_name] = df[col].shift(-days)
    if type(cols) == str:
        new_col_name = cols + "_shiftprev_" + str(days)
        df[new_col_name] = df[cols].shift(-days)
    return df

def rolling_mean(df, cols, days):
    if type(cols) == box.box_list.BoxList:
        for col in cols:
            new_col_name = col + "_mavg_" + str(days)
            df[new_col_name] = df[col].rolling(days).mean()
    if type(cols) == str:
        new_col_name = cols + "_mavg_" + str(days)
        df[new_col_name] = df[cols].rolling(days).mean()
    return df

def remove_by_value(df, cols, value):
    for col in cols:
        df = df[df[col] != value]
    return df

def remove_if_smaller(df, cols, value):
    if type(cols) == box.box_list.BoxList:
        for col in cols:
            df = df[df[col] > value]
    if type(cols) == str:
        df = df[df[cols] > value]
    return df

def remove_if_greater(df, cols, value):
    if type(cols) == box.box_list.BoxList:
        for col in cols:
            df = df[df[col] < value]
    if type(cols) == str:
        df = df[df[cols] < value]
    return df

def standardscaling(df, cols):
    scaler = StandardScaler().fit(df[cols])
    X_train_scaled = scaler.transform(df[cols])
    return X_train_scaled

def less_greater_encoding(df, cols, threshold):
    def func(cell):
        if cell >= threshold:
            return 1
        else:
            return 0

    if type(cols) == box.box_list.BoxList:
        for col in cols:
            new_col_name = col + "_lessgreatenc"
            df[new_col_name] = df.apply(lambda x: func(x[col]), axis=1)
    if type(cols) == str:
        new_col_name = cols + "_lessgreatenc"
        df[new_col_name] = df.apply(lambda x: func(x[cols]), axis=1)
    return df

def two_cols_percent_delta(df, base_col, second_col, new_col):
    df[new_col] = (df[second_col] / df[base_col]) * 100 - 100
    return df

def keep_dtype_only(df, cols, dtype):
    def type_check(x):
        return type(x) is eval(dtype)

    for col in cols:
        df = df[df[col].apply(lambda x: type_check(x))]
    return df

def set_col_dtype(df, cols, dtype):
    if type(cols) == box.box_list.BoxList:
        for col in cols:
            df[col] = df[col].astype(dtype)
    if type(cols) == str:
        df[cols] = df[cols].astype(dtype)
    return df

def fill_na_with_last_value(df, cols):
    """This function fills empty cells of column with last filled value.

    Args:
        df (pandas dataframe): The dataframe passed through the prep pipeline
        cols (BoxList or str): The Columns on which this function shall be applied
    """
    dfa = df.copy()
    df[cols] = dfa[cols].fillna(method='ffill')
    return df

def set_positive_values_to_zero(df, cols):
    def func(cell):
        if cell >= 0:
            return cell
        else:
            return 0

    if type(cols) == box.box_list.BoxList:
        for col in cols:
            df[col] = df.apply(lambda x: func(x[col]), axis=1)
    if type(cols) == str:
        df[cols] = df.apply(lambda x: func(x[cols]), axis=1)
    return df
    
def rename_col(df, old_colname, new_colname):
    df = df.rename(columns={old_colname: new_colname})
    return df

def lin_reg_of_col(df, X_cols, y_col, new_colname):
    # NA values are a problem here
    # Works only with date columns in X_cols
    reg = LinearRegression().fit(df[X_cols].apply(lambda x: float(x.strftime('%Y%d%m'))).values.reshape(-1, 1), df[y_col])
    df[new_colname] = reg.predict(df[X_cols].apply(lambda x: float(x.strftime('%Y%d%m'))).values.reshape(-1, 1))
    return df

