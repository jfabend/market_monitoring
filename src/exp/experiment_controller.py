import sys, getopt, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

from db.config import Config
from db.connect_db import DbConnection
from db.get_dbtable_data import get_dbtable_data
from exp.model import Model

import pandas as pd

# Read exp config yml
import yaml
from box import Box
with open(os.getenv("ROOT_DIR") + "\\exp\\exp_config.yml", "r") as ymlfile:
  exp_config = Box(yaml.safe_load(ymlfile))

# Read table from DB
data = get_dbtable_data(exp_config.base_table_name)

# Prepair model and param grid
models_to_apply = []
for modelname in exp_config.models:
    model_params = exp_config.models.get(modelname)
    next_model = Model(model_name = modelname, params = model_params)
    models_to_apply.append(next_model)

print(str(models_to_apply))

# Initialize a new Experiment Object
    # Arguments:
        # Feature List (X)
        # Base Table Name
        # Target Column (Y)
        # ETL Pipeline Configuration
        # Data Pipeline Configuration
        # Models and their params
