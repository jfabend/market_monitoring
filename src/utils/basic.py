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