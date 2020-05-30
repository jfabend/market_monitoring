import pandas as pd
import sys, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from db.get_dbtable_data import get_dbtable_data
from utils import basic
from dataprep import prep_funcs

pipe_config_pipe = "\\dataprep\\data_pipe.yml"
pipe_config = basic.read_config(pipe_config_pipe)
data = get_dbtable_data("joined_zwei")


def mean_by_group(df, cols):
    return df.groupby(cols).mean()

# pipeline
#df.pipe(mean_by_group, cols = 'hoch')
#.pipe(second_function)

def run_pipeline(df):
    tmp_df = df
    for pipe_obj in pipe_config:
        function = pipe_config.get(pipe_obj).func
        args = dict(pipe_config.get(pipe_obj))
        if len(args) is 1:
            print("no arguments")
            args = None
        else:
            del args['func']
            print(args)
        target_func = getattr(prep_funcs, function)
        if args:
            tmp_df = tmp_df.pipe(target_func, **args)
            print(tmp_df)
        else:
            tmp_df = tmp_df.pipe(target_func)
            print(tmp_df)
    return tmp_df

run_pipeline(data)