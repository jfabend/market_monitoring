from dotenv import load_dotenv
load_dotenv(verbose=False)
from db.connect_db import DbConnection
from db.execute_query import QueryExecution
import os

dbini_path = os.getenv("ROOT_DIR")

_DbConnection = DbConnection(dbini_path)
connection_objects = _DbConnection.setup_connection()
conn = connection_objects[0]
cur = connection_objects[1]

query_string = "CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);"

_QueryExecution = QueryExecution(conn, cur)
_QueryExecution.execute_query(query_string)