from sklearn import linear_model

class Model():

    def __init__(self, model_name, params):
        self.model_name = model_name
        self.params = params
    
    def return_model(self):
        if self.model_name is "lm":
            return_model = linear_model.LinearRegression(normalize=bool(self.params.normalize))
        return return_model