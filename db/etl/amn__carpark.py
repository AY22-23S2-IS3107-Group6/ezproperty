import pymongo
import pandas as pd
import mysql.connector
import requests
from sqlalchemy import create_engine



def extract():

    # Fetches daily token which is needed along with access key for API calls
    fetchTokenHeader = {'AccessKey': process.env.URA_API_ACCESSKEY}
    resp = requests.get('https://www.ura.gov.sg/uraDataService/insertNewToken.action', fetchTokenHeader) 
    URA_API_TOKEN = resp.json()['Result']

    # Setting up default header for API calls
    apiHeader = {'AccessKey': process.env.URA_API_ACCESSKEY, 'Token': URA_API_TOKEN}

    # Fetch both data sets
    respPublic = requests.get('https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details', apiHeader).json()
    respSeason = requests.get('https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Season_Car_Park_Details', apiHeader).json() 

    # Feed data into transformation
    transform(respPublic, respSeason)


def transform(respPublic, respSeason):
    # merge
    # convert variables accordingly
    # remove grouped carparks
    # flatten coordinates
    table_name = ""

    load(df, table_name)


def load(df, table_name):

    # Assume we just feed into mongodb first, or do we push into SQL here as well

    try:
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
            .format(user="",
            pw="",
            db=""))
        
        df.to_sql(table_name, con = engine, if_exists = "append", chunksize = 1000)
    except Exception as e:
        print("Data loading error: " + str(e))