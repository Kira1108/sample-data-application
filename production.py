from joblib import load
from config import MODEL_PATH
from extract import MysqlLoader
from db import db

model = load(MODEL_PATH)

def predict_price(table):
    df = MysqlLoader(f"select * from {table}").load()
    df['prediction'] = model.predict(df)
    db.write_df(df, f"{table}_predict")
    
    
def app():
    predict_price('brent')
    predict_price('wti')
    
if __name__ == "__main__":
    app()   
    

