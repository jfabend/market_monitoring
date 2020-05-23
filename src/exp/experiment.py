
from sklearn import model_selection as ms
class Experiment():

    def __init__(self, data, feature_list, base_table_name, target_col, etl_prep_config, model_prep_config, model, param_grid):
        self.data = data
        self.feature_list = feature_list
        self.target_col = target_col
        self.feature_data = data[feature_list]
        self.target_data = data[target_col]

        self.base_table_name = base_table_name
        self.etl_prep_config = etl_prep_config
        self.model_prep_config = model_prep_config
        self.model = model
        self.param_grid = param_grid
        return None

# Perfom gridsearch cross validation and evaluation
    def start(self):
        grid = ms.GridSearchCV(self.model, self.param_grid, cv=10, scoring='accuracy', return_train_score=False)
        grid.fit(self.feature_data, self.target_data) 