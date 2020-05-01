import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from utils import basic
from db.config import Config
from db.get_db_data import GetTableData

_GetTableData = GetTableData()
table_data = _GetTableData.create_pandas_table("SELECT * FROM futures_dax LIMIT 3;")

col_values = basic.inspect_pd_table(table_data)
print([basic.string_to_sql_type(col_value) for col_value in col_values])

_GetTableData.close_conn()



        # Herausfinden, wie die Datumspalte heißt
            # Man könnte auch einfach erstmal die erste Spalte nehmen
            # CASE für die Prüfung, ob das Date Format europäisch oder amerikanisch ist

        # Herausfinden, welche Datentypen die Spalten haben
            # Regex - enthält die Spalte Zahlen?
            # Regex - enthält die Spalten . oder , als Dezimalseperator
