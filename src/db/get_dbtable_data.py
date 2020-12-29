import pandas as pd
import psycopg2
import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

from utils import basic
from db.config import Config
from db.connect_db import DbConnection
from db.execute_query import QueryExecution
from db.get_db_data import GetTableData

def get_dbtable_data(tablename):

    connection_objects = basic.setup_db_connection()
    conn = connection_objects[0]
    cur = connection_objects[1]
    _GetTableData = GetTableData(conn, cur)

    query = f"SELECT * FROM {tablename};"

    df = _GetTableData.create_pandas_table(query)

    return df

