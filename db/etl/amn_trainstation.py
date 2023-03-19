import pymongo
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

def extract():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    # db name
    db = client["XXX"]
    # collection name
    collection = db["TrainStation"]
    all_records = collection.find()

    # load into pandas
    df = pd.DataFrame(list(all_records))

    # transform
    transform(df)

def transform(df):
    # transform magic in pandas
    # convert x, y to district?
    table_name = ""

    load(df, table_name)

def load(df, table_name):
    try:
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
            .format(user="",
            pw="",
            db=""))
        
        df.to_sql(table_name, con = engine, if_exists = "append", chunksize = 1000)
    except Exception as e:
        print("Data loading error: " + str(e))

def help():
        # think need to create table before connecting to mysql in load
    # create mysql table
        # convert x, y to district?
        sql = """CREATE TABLE TrainStation (
            id INT NOT NULL PRIMARY KEY,
            StationName VARCHAR(50) NOT NULL,
            StationNum VARCHAR(6) NOT NULL,
            X DECIMAL(9, 4) NOT NULL,
            Y DECIMAL(9, 4) NOT NULL,
            Latitude DECIMAL(10, 9) NOT NULL,
            Longitude DECIMAL(10, 9) NOT NULL,
            Colour VARCHAR(10) NOT NULL,
            District VARCHAR(20) NOT NULL
            );"""
        conn = mysql.connector.connect(
            host = "localhost", 
            user = "",
            password = "",
            db = "")
        
        cursor = conn.cursor()
        cursor.execute(sql)