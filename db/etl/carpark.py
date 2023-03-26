import pymongo
import pandas as pd
import requests
import json
from ..lake import DataLake
from ..warehouse import DataWarehouse

def extract():

    # Feed data into lake / mongoDB
    print("Carpark: Feeding data into lake")

    URA_API_ACCESSKEY = '84d7c27b-8dc6-4a34-9ea3-7769c174007c'

    # Fetches daily token which is needed along with access key for API calls
    fetchTokenHeader = {'Content-Type': 'application/json', 'AccessKey': URA_API_ACCESSKEY, 'Accept': 'application/json', 'User-Agent': 'PostmanRuntime/7.28.4'}
    resp = requests.get('https://www.ura.gov.sg/uraDataService/insertNewToken.action', headers = fetchTokenHeader) 

    print(resp)
    print(resp.json())

    URA_API_TOKEN = resp.json()['Result']
    

    # Setting up default header for API calls
    apiHeader = {'Content-Type': 'application/json', 'AccessKey': URA_API_ACCESSKEY, 'Token': URA_API_TOKEN, 'User-Agent': 'PostmanRuntime/7.30.1'}

    # Fetch both data sets
    respPublic = requests.get('https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details', headers = apiHeader)
    respSeason = requests.get('https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Season_Car_Park_Details', headers = apiHeader) 

    carparkPublic = respPublic.json()['Result']
    carparkSeason = respSeason.json()['Result']

    # Insert data
    db = DataLake()
    db.insert_to_schema("amn__CarparkPublic", carparkPublic)
    db.insert_to_schema("amn__CarparkSeason", carparkSeason)

    # Test query
    result = db.query_find("amn__CarparkPublic", 
        { "ppCode": "A0004" }
    )

    # Proof that query works
    for x in result:
        print(x)
    
    # Technically supposed to push in query result, but just feeding in data directly
    transform(carparkPublic, carparkSeason)


def transform(carparkPublic, carparkSeason):
   
    # Transform data accordingly
    print("Carpark: Transforming data")

    load(carparkPublic)


def load(result):

    # Load data into MySQL accordingly
    print("Carpark: Loading data")
    # print(result)

    # # result = list(map(lambda x: tuple(x.values()), result))
    # result = result.map(lambda x: tuple(x.values()))
    

    # print(result)

    # # Insert data
    # db = DataWarehouse()
    # db.insert_to_schema("test__Test", result)

    # # Query data using SQL
    # result = db.query('''
    #     SELECT * FROM test__Test
    # ''')

    # for x in result:
    #     print(x)


extract()


