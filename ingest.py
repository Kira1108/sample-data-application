from extract import CsvLoader
from db import db, init_db


def app(ds = "20220-05-01"):
    
    init_db()
    brent = CsvLoader('./data/brent.csv').load()
    wti = CsvLoader('./data/brent.csv').load()
    
    db.write_df(brent, 'brent')
    db.write_df(wti, 'wti')
    
    
if __name__ == "__main__":
    app()