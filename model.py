from abc import ABC, abstractmethod
from joblib import load
from datetime import datetime, timedelta
import pandas as pd


class Model(ABC):
    
    def fit(self,X, y = None):
        return self
    
    @abstractmethod
    def predict(self, X):
        ...
         
    def fit_predict(self, X, y = None):
        return self.fit(X, y).predict(X)
        
class MaPredictor(Model):
    
    def __init__(self,window):
        self.window = window
        
    def predict(self, X):
        return X['Price'].rolling(self.window).mean()
    

class ExpPredictor(Model):
    def __init__(self,  steps =20):
        self.steps = steps
        self.model = load("./models/exp.joblib")
        
    def predict(self, X):
        preds = self.model.predict(params=self.model.params, start=0, end=len(X) + self.steps - 1)
        
        prediction_df = pd.DataFrame(
            [X['Date'].iloc[-1] + timedelta(days = n) for n in range(1,21)],
            columns = ['Date'])
        
        pred_df = pd.concat([X, prediction_df])
        pred_df['prediction'] = preds
        return pred_df
        
        