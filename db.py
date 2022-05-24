from sqlalchemy import create_engine
from dataclasses import dataclass
import pandas as pd
import logging
import pymysql
logger = logging.getLogger(__name__)

@dataclass
class DBCONFIG:
    host:str = "localhost"
    user:str = "root"
    password:str = "root123"
    port:int = 5306
    db:str = "oil_price"

    def __post_init__(self):
        self.engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}")
        
    def write_df(self, df:pd.DataFrame, table:str, if_exists:str='replace', index:bool=False):
        logger.info(f"Writing to table: {table}")
        df.to_sql(table, con=self.engine, if_exists=if_exists, index=index)
        
    def read_sql_query(self, sql):
        with pymysql.connect(host = self.host, 
                             user = self.user, 
                             password = self.password, 
                             db = self.db, 
                             port = self.port) as conn:
            return pd.read_sql_query(sql, conn)
    
db = DBCONFIG()
    
def init_db():
    logger.info("Initializing Database...")
    engine = create_engine(f"mysql+pymysql://{db.user}:{db.password}@{db.host}:{db.port}")
    with engine.connect() as conn:
        conn.execute("CREATE DATABASE IF NOT EXISTS {};".format(db.db))
    logger.info("Initializing Database Done...")
        
if __name__ == "__main__":
    init_db()