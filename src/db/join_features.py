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

# Liste mit Feature-Spalten (c_bspstabelle.bspfeature) als Input Argument
class FeatureJoiner():

    def __init__(self):
        self.dbini_path = os.getenv("ROOT_DIR")
        self._DbConnection = DbConnection(self.dbini_path)

    def feature_join(self, feature_cols, exptablename):
        self.connection_objects = self._DbConnection.setup_connection()
        self.conn = self.connection_objects[0]
        self.cur = self.connection_objects[1]
        self.feature_cols = feature_cols
        self.exptablename = exptablename
        _GetTableData = GetTableData(self.conn, self.cur)

        _Config = Config()
        query_path = str(_Config.queries["get_col_data_types"])
        data_type_query = basic.read_query_file(query_path)

        query_path_dim_time = str(_Config.queries["get_dim_time_data_types"])
        data_type_query_dim_time = basic.read_query_file(query_path_dim_time)
        dim_time_type_df = _GetTableData.create_pandas_table(data_type_query_dim_time)
        print(dim_time_type_df.head())

        feature_colstring = ""
        for feature_col in feature_cols:
            idx = feature_cols.index(feature_col)
            tablename = feature_col.split(".")[0]
            colname = feature_col.split(".")[1]
            data_type_query_adj = data_type_query.replace("__tablename__", tablename).replace("__colname__", colname)
            col_type_df = _GetTableData.create_pandas_table(data_type_query_adj)

            feature_colstring = (feature_colstring
                                + col_type_df.ix[0, "table_name"]
                                + "__"
                                + col_type_df.ix[0, "column_name"]
                                + " "
                                + col_type_df.ix[0, "data_type"]
                                )
            if idx != (len(feature_cols) - 1):
                feature_colstring = feature_colstring + ", "
        
        print(feature_colstring)

        # BUILD LEFT JOIN STRING
            # LEFT JOIN PART
                #"LEFT_JOIN __feature_tablename__ ON (dime_time.date = __feature_tablename__.date);"

        self.cur.close()
        self.conn.close()

