from sklearn import linear_model

class Model():

    def __init__(self, model_name):
        self.model_name = model_name
    
    def return_model(self):
        if self.model_name == "lm":
            model = linear_model.LinearRegression()
        return model