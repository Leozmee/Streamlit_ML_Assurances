import pandas.core.frame as pcf
import sklearn.linear_model as skllm

class ExportData() :
    def __init__(self, param_model : skllm.Lasso, param_X_train : pcf.DataFrame, param_X_test : pcf.DataFrame, param_y_train: pcf.DataFrame, param_y_test : pcf.DataFrame) : 
        self.model = param_model 
        self.X_train = param_X_train
        self.X_test = param_X_test
        self.y_train = param_y_train
        self.y_test = param_y_test