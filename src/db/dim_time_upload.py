
import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

from utils import basic
from db.config import Config
from db.connect_db import DbConnection
from db.execute_query import QueryExecution

class DimTimeCreator():

    def __init__(self):
        self.dbini_path = os.getenv("ROOT_DIR")
        self._DbConnection = DbConnection(self.dbini_path)

    def dim_time_upload(self):
        self.connection_objects = self._DbConnection.setup_connection()
        self.conn = self.connection_objects[0]
        self.cur = self.connection_objects[1]

        _Config = Config()
        current_file_path = str(_Config.paths["dim_time_path"])
        query_path = str(_Config.queries["create_dim_time"])
        query_string = basic.read_query_file(query_path)


        colstring = ""
        table_name = ""
        final_query = basic.fill_up_query(query_string, colstring, table_name, current_file_path)

        print(final_query)

        _QueryExecution = QueryExecution(self.conn, self.cur)
        _QueryExecution.execute_query(final_query)

        self.cur.close()
        self.conn.close()

