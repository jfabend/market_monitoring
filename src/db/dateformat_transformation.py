import pandas as pd
import psycopg2
import sys, os
import logging
logging.basicConfig(level = logging.INFO)

from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

from db.get_dbtable_data import get_dbtable_data
from db.write_table import write_table
from db.execute_query import QueryExecution

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

query_path = str(_Config.queries["select_table_sample"])
query_string = basic.read_query_file(query_path)

def get_sta_dateformats(sta_table):
    query = query_string.replace("__tablename__", sta_table)
    query = query.replace("__limit__", "1000")
    df = _GetTableData.create_pandas_table(query)

    # determine the date formats for all table sample cells
    df['datetype'] = df.iloc[:,0].apply(lambda x: basic.string_to_sql_type(str(x)))
    
    # return the most presented date format
    major_dateformat = df['datetype'].value_counts(ascending=False).to_frame().index.values[0]

    return major_dateformat

def fill_datecol_with_zeros(day_o_month):
    if len(day_o_month) == 1:
        day_o_month = '0' + day_o_month
    return day_o_month


sta_tables_df["datetype"] = sta_tables_df['table_name'].apply(lambda x: get_sta_dateformats(x))
for tablename in sta_tables_df[(sta_tables_df["datetype"] == 'date__M/D/YYYY') | (sta_tables_df["datetype"] == 'date__D/M/YYYY')]['table_name']:

    logging.info(f'next table for date format transformation: {tablename}')


    # retrieve one M/D/YYYY table as pd dataframe
    sta_tablename = tablename

    test_dm_table = get_dbtable_data(sta_tablename)
    #test_dm_table

    # new data frame with split value columns 
    new = test_dm_table.iloc[:,0].str.split("/", n = 3, expand = True) 
    #new

    # making separate month column from new data frame 
    test_dm_table["month"] = new[0] 
    
    # making separate day column from new data frame 
    test_dm_table["day"] = new[1] 

    # making year column from new data frame 
    test_dm_table["year"] = new[2] 
    #test_dm_table

    test_dm_table['month_o'] = test_dm_table['month'].apply(lambda x: fill_datecol_with_zeros(x))
    test_dm_table['day_o'] = test_dm_table['day'].apply(lambda x: fill_datecol_with_zeros(x))

    test_dm_table['date'] = test_dm_table['month_o'] + '/' + test_dm_table['day_o'] + '/' + test_dm_table['year']
    test_dm_table.drop(['month', 'month_o', 'day_o', 'year', 'day'], axis=1, inplace=True)

    # mach die alte tabelle leer
    drop_tmp_query = " DROP TABLE IF EXISTS __tablename__;"
    _QueryExecution = QueryExecution(conn_cur_list[0], conn_cur_list[1])
    _QueryExecution.execute_query(drop_tmp_query.replace("__tablename__", sta_tablename))

    logging.info(f'date format transformation finished for: {tablename}')

    # füge die neuen bereinigten Daten ein
    from db.write_table import write_table
    write_table(test_dm_table, sta_tablename)

conn_cur_list[0].close()
conn_cur_list[1].close()