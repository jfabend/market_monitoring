import sys, getopt, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))

from db.config import Config
from db.connect_db import DbConnection
from db.get_dbtable_data import get_dbtable_data
from exp.model import Model
from exp.experiment import Experiment

import pandas as pd

# Read exp config yml
import yaml
from box import Box
with open(os.getenv("ROOT_DIR") + "\\exp\\exp_config.yml", "r") as ymlfile:
  exp_config = Box(yaml.safe_load(ymlfile))

# Read table from DB
data = get_dbtable_data(exp_config.table_name)

# Read features and target
feature_list = exp_config.feature_list
target = exp_config.target

# Prepair model and param grid
models_to_apply = []
for modelname in exp_config.models:

    # Create sklearn model object according to given model name
    # without any params (without further info, default values would be used)
    next_model_class = Model(model_name = modelname)
    next_model_object = next_model_class.return_model()
    models_to_apply.append(next_model_object)

    model_params_raw = exp_config.models.get(modelname)

  # Ich mache einen Datenerzeugungsschritt
    # Da wird die Feature Tabelle erzeugt
    # Dann wird über die Model Param Grids geloopt

#print(str(dict(model_params_raw)))
#print(data.head())
#print(feature_list)

experiment = Experiment(data=data,
                        feature_list=feature_list,
                        target_col=target,
                        model=models_to_apply[0],
                        param_grid=model_params_raw)
#print(type(experiment))

results = experiment.start()
results.head()