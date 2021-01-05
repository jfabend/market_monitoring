import sys, getopt, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

import logging

import configparser
from sqlalchemy import create_engine, text

logging.basicConfig(level = logging.INFO)

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

    # drop table if exists
    logging.info(f' dropping table {tablename} if it exists')
    #drop_str = 'DROP TABLE IF EXISTS __tablename__;'
    #sql = text(drop_str.replace('__tablename__', tablename))
    sql = text('DROP TABLE IF EXISTS sta_putcall_vix;')
    engine.execute(sql)

    # write df to database
    logging.info(f' writing prepped dataframe to database table {tablename}')
    df.to_sql(tablename, engine, index=False)
    
    logging.info("writing df into db was successful")