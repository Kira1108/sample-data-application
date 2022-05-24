import pandas as pd
from abc import ABC, abstractmethod
from db import db


class DataLoader(ABC):
    
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        ...
        
    def transform(self, df:pd.DataFrame) -> pd.DataFrame:
        return df
    
    def load(self):
        return self.transform(self.extract())  
    

class CsvLoader(DataLoader):
    
    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.args = args
        self.kwargs = kwargs
    
    def extract(self) -> pd.DataFrame:
        """Load oil price json file."""
        return pd.read_csv(self.path, *self.args, **self.kwargs)
    

    def transform(self, df) -> pd.DataFrame:
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    
class MysqlLoader(DataLoader):
    
    def __init__(self, sql):
        self.sql = sql
    
    def extract(self) -> pd.DataFrame:
        df = db.read_sql_query(self.sql)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    
    
    
    
