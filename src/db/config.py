import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

class Config():
    def __init__(self):
        self.root = os.getenv("ROOT_DIR")

    @property
    def queries(self):
        query_dict = {
            "create_update_dict":self.root + "\\db\\sql\\Insert_Delta.txt"
        }
        return query_dict