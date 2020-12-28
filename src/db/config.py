import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

class Config():
    def __init__(self):
        self.root = os.getenv("ROOT_DIR")
        self.global_dir = os.getenv("GLOBAL_DIR")

    @property
    def queries(self):
        query_dict = {
            "create_update": self.root + "\\db\\sql\\Insert_Delta.txt",
            "create_dim_time": self.root + "\\db\\sql\\dim_time.txt",
            "get_col_data_types": self.root + "\\db\\sql\\col_data_types.txt",
            "get_dim_time_data_types": self.root + "\\db\\sql\\dim_time_col_data_types.txt",
            "get_sta_tables": self.root + "\\db\\sql\\get_sta_tables.txt"
        }
        return query_dict

    @property
    def paths(self):
        path_dict = {
            "dim_time_path": self.global_dir + "\\dim_time\\dim_time.csv",
        }
        return path_dict