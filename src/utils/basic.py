#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import csv
import string
import re
import pandas as pd

def get_folder_files(foldername, pattern = '*'):
    #return glob.glob(foldername + pattern)
    return glob.glob(foldername + '/**/' + pattern, recursive=True)

def get_parent_folder(path):
    if "\\" in path:
        path_components = path.split("\\")
    if "/" in path:
        path_components = path.split("/")
    return path_components[-2]

def get_file_headers(path):
    #printable = set(string.printable)
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
    f = open(path,"r")
    return f.read()

def convert_headers_to_colstring(headers):
    colstring = ""
    for col in headers:
        if headers.index(col) == 0:
            colstring = colstring + " " + col.replace("'", "") + " varchar"
        else:
            colstring = colstring + ", " + col.replace("'", "") + " varchar"
    return colstring.lower()

def fill_up_query(query_template, colstring, tablename, filepath):
    step_one = query_template.replace("__columnstring__", colstring)
    step_two = step_one.replace("__tablename__", tablename)
    step_three = step_two.replace("__filepath__", filepath)
    if "datum" in colstring:
        step_four = step_three.replace("__idcol__", "datum")
    if "date" in colstring:
        step_four = step_three.replace("__idcol__", "date")
    return step_four

def delete_na_from_csv(file_path):
    df = pd.read_csv(file_path, sep=',').dropna()
    df.to_csv(file_path, index=False)

def value_sample_pd_table(pd_df):
    col_list = list(pd_df.columns)   # - with colnames
    # result = [pd_df.loc[[0], [col]] for col in col_list] - first cell, but including colname
    result = [pd_df.ix[0, col] for col in col_list]   # first cell value
    return result

def cols_pd_table(pd_df):
    return list(pd_df.columns)

def string_to_sql_type(string):

    # date regex
    german_date_one = re.findall('^\d\d\.\d\d\.20\d\d$', string)
    german_date_two = re.findall('^\d\d\.\d\d\.19\d\d$', string)
    us_date_one = re.findall('^19\d\d-\d\d-\d\d$', string)
    us_date_two = re.findall('^20\d\d-\d\d-\d\d$', string)

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
    if us_decimal_one or us_decimal_two or us_decimal_three or us_decimal_four:
        return 'us_decimal'
    if numeric_one or us_numeric_one or eu_numeric_one:
        return 'numeric'
    if eu_decimal_one or eu_decimal_two:
        return 'eu_decimal'
    else:
        return 'varchar'

def form_main_part_core_query(cols, target_types, tablename):
    query = " INSERT INTO c___tablename__ SELECT "
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
    date_col_index = [target_types.index(coltype) for coltype in target_types  if 'date' in coltype][0]
    date_col = cols[date_col_index]
    date_format = [coltype.replace("date__", "") for coltype in target_types  if 'date' in coltype][0]
    query = (" LEFT JOIN c___tablename__ ON c___tablename__.date = TO_DATE(__tablename__."
            + date_col
            + ", '" + date_format + "')"
            + " WHERE c___tablename__.date is NULL;")
    query = query.replace("__tablename__", tablename)
    return query
