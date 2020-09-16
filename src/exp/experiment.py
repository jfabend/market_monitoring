
from sklearn import model_selection as ms
import pandas as pd

class Experiment():

    def __init__(self, data, feature_list, target_col, model, param_grid):
        """[summary]

        Args:
            data (dataframe): dataframe including the data for train and test
            feature_list (list): list of features
            target_col (str): name of target column
            model (Object): Model Object created with sklearn
            param_grid (dict): Dict or list of dicts including the model params names as keys and a list of values as value

        Returns:
            Object: Object of class Experiment
        """
        self.data = data
        self.feature_list = feature_list
        self.target_col = target_col
        self.feature_data = data[feature_list]
        self.target_data = data[target_col]

        self.model = model
        self.param_grid = param_grid
        return None

# Perfom gridsearch cross validation and evaluation
    def start(self):
        grid = ms.GridSearchCV(self.model, self.param_grid, cv=10, scoring='accuracy', return_train_score=False)
        grid.fit(self.feature_data, self.target_data)

        results = pd.DataFrame(grid.cv_results_)[['mean_test_score', 'std_test_score', 'params']] 
        return results