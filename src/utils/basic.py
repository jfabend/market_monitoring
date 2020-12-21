#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import csv
import string
import re
import pandas as pd
import os

def get_folder_files(foldername, pattern = '*'):
    """returns a list of the names of the files in the given folder.

    Arguments:
        foldername {str} -- name of the folder which should be browsed for files

    Keyword Arguments:
        pattern {str} -- regex pattern which is used for finding certain files (default: {'*'})

    Returns:
        [list] -- list of names of the files in the given folder
    """
    return glob.glob(foldername + '/**/' + pattern, recursive=True)

def get_parent_folder(path):
    """Returns the superior folder / parent folder of a given folder

    Args:
        path (str): the path of the child folder

    Returns:
        str: path of the parent folder / superior folder
    """
    if "\\" in path:
        path_components = path.split("\\")
    if "/" in path:
        path_components = path.split("/")
    return path_components[-2]

def get_file_headers(path):
    """Returns the headers of a csv file for naming db columns.

    It also removes special characters which should not be used as db col names.
    If there is only an empty string left as header of a certain column,
    the function returns 'leer' as header name for that column.

    Args:
        path (str): path to the csv file

    Returns:
        list: list of the headers of the csv file
    """
    with open(path, 'r') as f:
        d_reader = csv.DictReader(f)
        header = d_reader.fieldnames
        header_decoded = []
        for col in header:
            col_only_letters = re.sub(r'[^a-zA-Z]',r'', col.replace("\W", ""))
            if not col_only_letters:
                col_only_letters = 'leer'
            header_decoded.append(col_only_letters)
            
    return header_decoded

def read_query_file(path):
    """Just returns the content of a txt file.
    
    Other file formats might work, too. Not tested yet.

    Args:
        path (str): path to a txt file

    Returns:
        str: string with all the content of the file
    """
    f = open(path,"r")
    return f.read()

def convert_headers_to_colstring(headers):
    """Adds commas and the datatype varchar to a list of file headers to use that string in queries.

    Args:
        headers (list): List of headers of a file

    Returns:
        str: the db column names and its datatyoe varchar to be used in CREATE Statements
    """
    colstring = ""
    for col in headers:
        if headers.index(col) == 0:
            colstring = colstring + " " + col.replace("'", "") + " varchar"
        else:
            colstring = colstring + ", " + col.replace("'", "") + " varchar"
    return colstring.lower()

def fill_up_query(query_template, colstring, tablename, filepath):
    """Replaces placeholders in a COPY TO postgres query with actual tablename, file, and col names.

    Args:
        query_template (str): Query String including placeholders
        colstring (str): db column names separated by commas
        tablename (str): db tablename
        filepath ([type]): path to the file which should be copied to the db

    Returns:
        str: Query including specific tablename, cols and a certain filepath
    """
    step_one = query_template.replace("__columnstring__", colstring)
    step_two = step_one.replace("__tablename__", tablename)
    step_three = step_two.replace("__filepath__", filepath)
    step_four = step_three.replace("__idcol__", colstring.split(" ")[1])
    #if "datum" in colstring:
    #    step_four = step_three.replace("__idcol__", colstring[0])
    #if "date" in colstring:
    #    step_four = step_three.replace("__idcol__", colstring[0])
    #if colstring is "":
    #    step_four = step_three
    #else:
    #    step_four = step_three
    return step_four

def delete_na_from_csv(file_path):
    """Delete rows with missing values from a csv file.

    Args:
        file_path (str): path to csv file
    """
    df = pd.read_csv(file_path, sep=',').dropna()
    df.to_csv(file_path, index=False)

def value_sample_pd_table(pd_df):
    """Return the first row of a dataframe.

    Args:
        pd_df (df): pandas dataframe

    Returns:
        df: pandas dataframe (one row)
    """
    col_list = list(pd_df.columns)   # - with colnames
    # result = [pd_df.loc[[0], [col]] for col in col_list] - first cell, but including colname
    result = [pd_df.loc[0, col] for col in col_list]   # first cell value
    return result

def cols_pd_table(pd_df):
    """Returns column names of a pandas dataframe as a list

    Args:
        pd_df (dataframe): Pandas dataframe

    Returns:
        list: list of column names
    """
    return list(pd_df.columns)

def string_to_sql_type(string):
    """Analyses a string and returns a suitable sql datatype

    Args:
        string (str): a string representing a cell value of the target column

    Returns:
        str: the guessed sql datatype
    """
    # https://www.postgresqltutorial.com/postgresql-to_char/
    # https://www.rexegg.com/regex-quickstart.html

    # date regex
    german_date_one = re.findall('^\d\d\.\d\d\.20\d\d$', string)
    german_date_two = re.findall('^\d\d\.\d\d\.19\d\d$', string)
    #us_date_one = re.findall('^19\d\d-\d\d-\d\d$', string)
    us_date_one = re.findall('^19\d\d-(0[1-9]|1[012])-\d\d$', string)
    #us_date_two = re.findall('^20\d\d-\d\d-\d\d$', string)
    us_date_two = re.findall('^20\d\d-(0[1-9]|1[012])-\d\d$', string)
    us_date_three = re.findall('^\D{3} \d\d, 20\d\d$', string)
    us_date_four = re.findall('^\D{3} \d\d, 19\d\d$', string)
    us_date_five = re.findall('^\d\d-\D{3}-19\d\d', string)
    us_date_six = re.findall('^\d\d-\D{3}-20\d\d', string)
    us_date_seven = re.findall('^(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])/(19|20)\d\d$', string)
    us_date_eight = re.findall('(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$', string)

    #us_date_seven = re.findall()

    # float regex
    us_decimal_one = re.findall('^\d+.\d{1,2}$', string)               # 29.99
    us_decimal_two = re.findall('^\d+,\d{3}.\d{1,2}$', string)           # 140,000.99
    us_decimal_three = re.findall('^\d+,\d{3},\d{3}.\d{1,2}$', string)    # 140,000,000.99
    us_decimal_four = re.findall('^\d+,\d{3},\d{3},\d{3}.\d{1,2}$', string)    # 140,000,000,000.99

    numeric_one = re.findall('^\d+$', string)                                 # 45
    us_numeric_one = re.findall('^\d+,\d{3}$', string)
    eu_numeric_one = re.findall('^\d+.\d{3}$', string)

    eu_decimal_one = re.findall('^\d+,\d{1,2}$', string)
    eu_decimal_two = re.findall('^\d+.\d{3},\d{1,2}$', string)  

    if german_date_one or german_date_two:
        return 'date__DD.MM.YYYY'
    if us_date_one or us_date_two:
        return 'date__YYYY-MM-DD'
    if us_date_three or us_date_four:
        return 'date__Mon DD, YYYY'
    if us_date_five or us_date_six:
        return 'date__DD-Mon-YYYY'
    if us_date_seven:
        return 'date__MM/DD/YYYY'
    if us_date_eight:
        return 'date__DD/MM/YYYY'
    if us_decimal_one or us_decimal_two or us_decimal_three or us_decimal_four:
        return 'us_decimal'
    if numeric_one or us_numeric_one or eu_numeric_one:
        return 'numeric'
    if eu_decimal_one or eu_decimal_two:
        return 'eu_decimal'
    else:
        return 'varchar'

def form_main_part_core_query(cols, target_types, tablename):
    """Builds a sql query for inserting data from a staging table in db to a core table.

    All data types in staging tables are varchar. The data types of core tables should be
    corresponding to its content. This function gets the target data types as argument and
    casts the column content of the staging table to its new data type.

    The target data types are determined in the string_to_sql_type function.

    Args:
        cols (list): list of column names
        target_types (list): list of the target data types of the columns given in the first argument
        tablename (str): tablename suffix without the staging prefix sta_ or the core prefix c_.

    Returns:
        str: Insert into core table query 
    """
    query = " INSERT INTO c___tablename__ SELECT "
    query = query.replace("__tablename__", (tablename))
    tablename = "sta_" + tablename
    query = query.replace("__tablename__", tablename)
    for col in cols:
        idx = cols.index(col)
        if idx != (len(cols) - 1):
            if 'date' in target_types[idx]:
                query = query + "TO_DATE(" + tablename + "." + col + ", '" + target_types[idx].replace("date__", "") + "')" + " AS " + "date"
            if target_types[idx] is 'numeric' or 'decimal' in target_types[idx]:
                if 'eu_' in target_types[idx]:
                    query = query + "CAST(REPLACE(REPLACE(" + tablename + "." + col + ", '.', ''), ',', '.') AS double precision)" + " AS " + col                  
                else:
                    query = query + "CAST(" + tablename + "." + col + " AS double precision)" + " AS " + col
            if 'date'not in target_types[idx] and 'numeric' not in target_types[idx] and 'decimal' not in target_types[idx]:
                query = query + tablename + "." + col + " AS " + col
            query = query + ", "
        else:
            if 'date' in target_types[idx]:
                query = query + "TO_DATE(" + tablename + "." + col + ", '" + target_types[idx].replace("date__", "") + "')" + " AS " + "date"
            if target_types[idx] is 'numeric' or 'decimal' in target_types[idx]:
                if 'eu_' in target_types[idx]:
                    query = query + "CAST(REPLACE(REPLACE(" + tablename + "." + col + ", '.', ''), ',', '.') AS double precision)" + " AS " + col                 
                else:
                    query = query + "CAST(" + tablename + "." + col + " AS double precision)" + " AS " + col
            if 'date'not in target_types[idx] and 'numeric' not in target_types[idx] and 'decimal' not in target_types[idx]:
                query = query + tablename + "." + col + " AS " + col
    query = query + " FROM " + tablename
    return query

def form_create_part_core_query(cols, target_types, tablename):
    """Builds the sql query for creating the core table.

    The data types of core tables should be corresponding to its content.
    They are determined in the string_to_sql_type function and have to be
    inserted behind their column names in the CREATE statement.

    Args:
        cols (list): list of db column names
        target_types (list): list of the target data types of the columns given in the first argument
        tablename (str): tablename suffix without the staging prefix sta_ or the core prefix c_.

    Returns:
        str: CREATE core table statement
    """
    query = "CREATE TABLE IF NOT EXISTS __tablename__ ( "
    query = query.replace("__tablename__", ("c_" + tablename))
    for col in cols:
        idx = cols.index(col)
        if idx != (len(cols) - 1):
            if 'date' in target_types[idx]:
                query = query + "date" + " date, "
            if target_types[idx] is 'numeric' or 'decimal' in target_types[idx]:
                query = query +  col + " double precision, "
            if 'date'not in target_types[idx] and 'numeric' not in target_types[idx] and 'decimal' not in target_types[idx]:
                query = query +  col + " varchar, "
        else:
            if 'date' in target_types[idx]:
                query = query +  "date" + " date"
            if target_types[idx] is 'numeric' or 'decimal' in target_types[idx]:
                query = query +  col + " double precision"
            if 'date'not in target_types[idx] and 'numeric' not in target_types[idx] and 'decimal' not in target_types[idx]:
                query = query +  col + " varchar"
    query = query + ");"
    return query

def form_join_part_core_query(cols, target_types, tablename):
    """Builds the LEFT JOIN part of the join query for joining features from core tables.

    In these queries you can have lofts of components including
    LEFT JOIN new_table on ... Left JOIN next_table on ... etc.
    This function builds this part of the query.

    Args:
        cols ([type]): [description]
        target_types ([type]): [description]
        tablename ([type]): [description]

    Returns:
        [type]: [description]
    """
    date_col_index = [target_types.index(coltype) for coltype in target_types  if 'date' in coltype][0]
    date_col = cols[date_col_index]
    date_format = [coltype.replace("date__", "") for coltype in target_types  if 'date' in coltype][0]
    query = (" LEFT JOIN c___tablename__ ON c___tablename__.date = TO_DATE(sta___tablename__."
            + date_col
            + ", '" + date_format + "')"
            + " WHERE c___tablename__.date is NULL;")
    query = query.replace("__tablename__", tablename)
    return query

def read_config(path):
    """Reads config file and returns the content as list-kinda object

    Afterwards, you can retrieve content out of the config object by the syntax cfg_obj.param_area.param

    Args:
        path (str): path to config file

    Returns:
        list: config list object
    """
    # Read exp config yml
    import yaml
    from box import Box
    with open(os.getenv("ROOT_DIR") + path, "r") as ymlfile:
        exp_config = Box(yaml.safe_load(ymlfile))
    return exp_config