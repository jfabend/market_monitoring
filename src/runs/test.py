import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from utils import basic
from db.config import Config
from db.get_db_data import GetTableData

# Get all staging tables from the database

# for table in tables

tablename = "futures_dax"
query_inspect = "SELECT * FROM __tablename__ LIMIT 3;"
query_inspect = query_inspect.replace("__tablename__", tablename)

_GetTableData = GetTableData()
table_data = _GetTableData.create_pandas_table(query_inspect)
# table_data = _GetTableData.create_pandas_table("SELECT * FROM futures_dax LIMIT 3;")

col_values = basic.value_sample_pd_table(table_data)
cols = basic.cols_pd_table(table_data)
target_types = [basic.string_to_sql_type(col_value) for col_value in col_values]

#print(target_types)

create_part_core_query = basic.form_create_part_core_query(cols, target_types, tablename)
main_part_core_query = basic.form_main_part_core_query(cols, target_types, tablename)
join_part_core_query = basic.form_join_part_core_query(cols, target_types, tablename)

print(create_part_core_query + main_part_core_query + join_part_core_query)

_GetTableData.close_conn()

