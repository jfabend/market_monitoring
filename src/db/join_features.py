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

        # Read query template for inspecting datatypes of a db table 
        query_path = str(_Config.queries["get_col_data_types"])
        data_type_query = basic.read_query_file(query_path)

        # Read query for inspecting datatypes of the dim_time table
        query_path_dim_time = str(_Config.queries["get_dim_time_data_types"])
        data_type_query_dim_time = basic.read_query_file(query_path_dim_time)
        dim_time_type_df = _GetTableData.create_pandas_table(data_type_query_dim_time)

        # Build a string including the dim_time colnames and their datatypes
        dim_time_type_df["colstring_underscore"] = dim_time_type_df["table_name"] + "_" + dim_time_type_df["column_name"] + " " + dim_time_type_df["data_type"] + ", "
        dim_time_type_df["colstring_dot"] = dim_time_type_df["table_name"] + "." + dim_time_type_df["column_name"] + ", "
        dim_time_colstring = dim_time_type_df["colstring_underscore"].str.cat(sep=' ') #[0:-2]
        dim_time_colstring_dot = dim_time_type_df["colstring_dot"].str.cat(sep=' ') #[0:-2]
        tmp_colstring = dim_time_colstring_dot.replace("dim_time.", "tmp.dim_time_").replace("date", "dim_time_date").replace("dim_time_dim_time_", "dim_time_")

        # Build a string including the features colnames and their datatypes
        feature_colstring = ""
        feature_tables = []
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

            feature_tables.append(tablename)
        
        # Build CREATE statement
        create_query_target = "CREATE TABLE IF NOT EXISTS " + self.exptablename + " (" + dim_time_colstring + " " + feature_colstring + ");"
        create_query_tmp = "CREATE TABLE IF NOT EXISTS tmp (" + dim_time_colstring + " " + feature_colstring + ");"
        #print(create_query_target)
        #print(create_query_tmp)

        # Build INSERT tmp statement
        insert_query_part_one = ("INSERT INTO tmp"
                                + " ( SELECT " + dim_time_colstring_dot + " " + ', '.join(self.feature_cols)
                                + " FROM dim_time "
                                )
        unique_feature_tables = list(set(feature_tables))
        insert_query_part_two = ' '.join([("LEFT JOIN " + feature_table + " ON ( " + feature_table + ".date = dim_time.date)")  for feature_table in unique_feature_tables])
        insert_query_tmp = insert_query_part_one + insert_query_part_two + ");"
        #print(insert_query_tmp)

        # Build INSERT target statement
        insert_query_target = ("INSERT INTO " + self.exptablename
                                + " SELECT " + tmp_colstring + " " + ', '.join(self.feature_cols).replace(".", "__").replace("c_", "tmp.c_")
                                + " FROM tmp"
                                + " LEFT JOIN " + self.exptablename + " USING (dim_time_date)"
                                + " WHERE " + self.exptablename + ".dim_time_date IS NULL;"
                                )

        drop_tmp_query = " DROP TABLE IF EXISTS tmp;"
        final_query = create_query_target + " " +  create_query_tmp + " " + insert_query_tmp + " " + insert_query_target + " " + drop_tmp_query 
        print(final_query)

        _QueryExecution = QueryExecution(self.conn, self.cur)
        _QueryExecution.execute_query(final_query)

        self.cur.close()
        self.conn.close()

