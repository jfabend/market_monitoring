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

    def __init__(self):
        self.dbini_path = os.getenv("ROOT_DIR")
        self._DbConnection = DbConnection(self.dbini_path)
        self.connection_objects = self._DbConnection.setup_connection()
        self.conn = self.connection_objects[0]
        self.cur = self.connection_objects[1]

    # A function that takes in a PostgreSQL query and outputs a pandas database 
    def create_pandas_table(self, sql_query):
        table = pd.read_sql_query(sql_query, self.conn)
        return table

    def close_conn(self):
        self.cur.close()
        self.conn.close()


