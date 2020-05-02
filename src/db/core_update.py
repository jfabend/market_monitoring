import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
import pandas as pd
import numpy as np

from utils import basic
from db.config import Config
from db.connect_db import DbConnection
from db.execute_query import QueryExecution
from db.get_db_data import GetTableData

class CoreUpdate():

    def __init__(self):
        self.dbini_path = os.getenv("ROOT_DIR")
        self._DbConnection = DbConnection(self.dbini_path)

    def core_update(self):
        self.connection_objects = self._DbConnection.setup_connection()
        self.conn = self.connection_objects[0]
        self.cur = self.connection_objects[1]

        _GetTableData = GetTableData(self.conn, self.cur)
        # Get all staging tables from the database
        get_tables_query = "select * from information_schema.tables WHERE LEFT(table_name, 4) = 'sta_';"
        tables_pd = _GetTableData.create_pandas_table(get_tables_query)
        tables = tables_pd['table_name'].tolist()

        for table in tables:

            tablename = table
            query_inspect = "SELECT * FROM __tablename__ LIMIT 3;"
            query_inspect = query_inspect.replace("__tablename__", tablename)



            table_data = _GetTableData.create_pandas_table(query_inspect)
            #table_data = _GetTableData.create_pandas_table("SELECT * FROM futures_dax LIMIT 3;")

            col_values = basic.value_sample_pd_table(table_data)
            cols = basic.cols_pd_table(table_data)
            target_types = [basic.string_to_sql_type(col_value) for col_value in col_values]

            #print(target_types)
            
            tablename = tablename.replace("sta_", "")
            create_part_core_query = basic.form_create_part_core_query(cols, target_types, tablename)
            main_part_core_query = basic.form_main_part_core_query(cols, target_types, tablename)
            join_part_core_query = basic.form_join_part_core_query(cols, target_types, tablename)
            
            final_query = create_part_core_query + main_part_core_query + join_part_core_query
            print(final_query)

            _QueryExecution = QueryExecution(self.conn, self.cur)
            _QueryExecution.execute_query(final_query)

        self.cur.close()
        self.conn.close()

