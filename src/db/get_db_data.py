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

class GetTableData():

    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur


    def create_pandas_table(self, sql_query):
        """A function that takes a PostgreSQL select query
        and returns a pandas dataframe including the selected data

        Args:
            sql_query (str): select statement

        Returns:
            pandas df: data returned by the select query
        """
        table = pd.read_sql_query(sql_query, self.conn)
        return table

    def close_conn(self):
        self.cur.close()
        self.conn.close()


