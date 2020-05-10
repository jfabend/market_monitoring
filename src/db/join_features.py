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

    def feature_join(self, feature_cols):
        self.connection_objects = self._DbConnection.setup_connection()
        self.conn = self.connection_objects[0]
        self.cur = self.connection_objects[1]
        self.feature_cols = feature_cols

        tablenames = []
        for feature_col in feature_cols:
            tablename = feature_col.split(".")[0]
            tablenames.append(tablename)

        _GetTableData = GetTableData(self.conn, self.cur)
        get_table_heads_query = "select * from __c_tablename__ LIMIT 31;"

        for tablename in tablenames:
            get_table_head_query = get_table_heads_query.replace("__c_tablename__", tablename)
            table_head = _GetTableData.create_pandas_table(get_table_head_query)
            print(table_head.ix[0:30, "date"])

            #col_values = basic.value_sample_pd_table(table_head)
            #print(col_values)
            #target_types = [basic.string_to_sql_type(col_value) for col_value in col_values]
            #print(target_types)

        self.cur.close()
        self.conn.close()
# Sub Funktion
    # tablename als Input Argument

    # Liste oder DB Tabelle erstellen
        # 
        # basic.value_sample_pd_table(pd_df)
        # Wie frequent werden die Daten von __tablename__ aufgezeichnet?
        # Wie ist ihr Datumsformat? basic.string_to_sql_type

