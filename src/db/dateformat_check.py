#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import re
import pandas as pd
import os

from utils import basic
from db.get_db_data import GetTableData
from db.config import Config
_Config = Config()

# setup db connection
conn_cur_list = basic.setup_db_connection()
query_path = str(_Config.queries["get_sta_tables"])
query_string = basic.read_query_file(query_path)

# create 
_GetTableData = GetTableData(conn_cur_list[0], conn_cur_list[1])
sta_tables_df = _GetTableData.create_pandas_table(query_string)
_GetTableData.close_conn()

print(sta_tables_df.head())


# def determine_date_format()
