from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBRegressor
from xgboost import XGBClassifier

class Model():

    def __init__(self, model_name):
        self.model_name = model_name
    
    def return_model(self):
        if self.model_name == "linearmodel":
            model = linear_model.LinearRegression()
        if self.model_name == "randomforestregressor":
            model = RandomForestClassifier()
        if self.model_name == "xgboostregressor":
            model = XGBRegressor(objective='reg:squarederror')
        if self.model_name == "logisticregression":
            model = linear_model.LogisticRegression()
        if self.model_name == "xgboostclassifier":
            model = XGBClassifier()
        return model