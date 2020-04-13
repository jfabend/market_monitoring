from dotenv import load_dotenv
load_dotenv(verbose=False)
from db.connect_db import DbConnection
import os

dbini_path = os.getenv("ROOT_DIR")

_DbConnection = DbConnection(dbini_path)
print(str(_DbConnection.config()))
