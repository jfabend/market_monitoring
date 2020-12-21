
import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

from utils import basic
from db.config import Config
from db.connect_db import DbConnection
from db.execute_query import QueryExecution

class DeltaUploader():

    def __init__(self):
        self.dbini_path = os.getenv("ROOT_DIR")
        self._DbConnection = DbConnection(self.dbini_path)

    def delta_upload(self, current_file_path):
        self.connection_objects = self._DbConnection.setup_connection()
        self.conn = self.connection_objects[0]
        self.cur = self.connection_objects[1]

        headers = basic.get_file_headers(current_file_path)
        print("File headers: " + str(headers))
        if len(headers) <= 1:
            return

        #basic.delete_na_from_csv(current_file_path)

        colstring = basic.convert_headers_to_colstring(headers)
        print("Colstring: " + colstring)

        table_name = basic.get_parent_folder(current_file_path)
        print("tablename: " + table_name)

        _Config = Config()
        query_path = str(_Config.queries["create_update"])
        query_string = basic.read_query_file(query_path)

        final_query = basic.fill_up_query(query_string, colstring, table_name, current_file_path)

        print(final_query)

        _QueryExecution = QueryExecution(self.conn, self.cur)
        _QueryExecution.execute_query(final_query)

        self.cur.close()
        self.conn.close()

