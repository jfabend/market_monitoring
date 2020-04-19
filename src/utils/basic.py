#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import csv
import string
import re

def get_folder_files(foldername, pattern = '*'):
    return glob.glob(foldername + pattern)

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
    return colstring
    #string = "'date'"
    #rint(string.replace("'", ""))