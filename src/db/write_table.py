import sys, getopt, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

import configparser
from sqlalchemy import create_engine

def write_table(df, tablename):
    """Writes Pandas Dataframe to a Postgres DB.

    Arguments:
        df {pandas df} -- a dataframe to be written into a db
        tablename {str} -- the name for the target table in the db
    """
    # read config
    config = configparser.ConfigParser()
    config.read(os.getenv("ROOT_DIR") + '\\db\\database.ini')
    host = config['postgresql']['host']
    database = config['postgresql']['database']
    user = config['postgresql']['user']
    pw = config['postgresql']['password']
    port = config['postgresql']['port']
    pg_string = f'postgresql://{user}:{pw}@{host}:{port}/{database}'

    # init sqlalchemy write engine
    engine = create_engine(pg_string)
    df.to_sql(tablename, engine)
    
    print("writing df into db was successful")