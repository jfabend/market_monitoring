import pandas as pd
import psycopg2
import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

from utils import basic
from db.config import Config
_Config = Config()
from db.connect_db import DbConnection
from db.execute_query import QueryExecution
from db.get_db_data import GetTableData

def get_dbtable_sample(tablename, limit):
    """retrieves a limited sample of a db table

    Args:
        tablename (str): name of the desired table
        limit (str): desired amount of rows 

    Returns:
        pandas dataframe: db table sample
    """
    connection_objects = basic.setup_db_connection()
    _GetTableData = GetTableData(connection_objects[0], connection_objects[1])

    query = str(_Config.queries["select_table_sample"])
    query = query.replace("__tablename__", tablename)
    query = query.replace("__limit__", limit)

    df = _GetTableData.create_pandas_table(query)
    _GetTableData.close_conn()

    return df

