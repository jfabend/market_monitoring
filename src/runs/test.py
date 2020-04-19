import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from utils import basic
from db.config import Config

current_file_path = 'C:\\Users\\jonat\\OneDrive\\Trading\\Scoring und Marktüberwachung\\rohdaten\\futures_dax\\200903_202004.csv'

headers = basic.get_file_headers(current_file_path)

colstring = basic.convert_headers_to_colstring(headers)
table_name = basic.get_parent_folder(current_file_path)

_Config = Config()
query_path = str(_Config.queries["create_update"])
query_string = basic.read_query_file(query_path)

final_query = basic.fill_up_query(query_string, colstring, table_name, current_file_path)