import pandas as pd
import mysql.connector
import requests
from ..lake import DataLake


def extract():

    # Fetch data sets
    # Seems to be limited by MongoDB's 100 BSON limit
    # resp = requests.get(
    #     'https://data.gov.sg/api/action/datastore_search?resource_id=3561a136-4ee4-4029-a5cd-ddf591cce643'
    # )

    # But this works and I can insert 228 records
    resp = requests.get(
        'https://data.gov.sg/api/action/datastore_search?resource_id=3561a136-4ee4-4029-a5cd-ddf591cce643&limit=258'
    )

    # print(resp)
    # print(resp.json())
    respSuperMarket = resp.json()['result']['records']
    print(respSuperMarket)

    # Feed data into transformation
    transform(respSuperMarket)


def transform(respSuperMarket):

    # no transformation required
    load(respSuperMarket)


def load(respSuperMarket):

    # load into mongodb
    db = DataLake()
    db.insert_to_schema("amn__SuperMarket", respSuperMarket)

    testResult = db.query_find("amn__SuperMarket", {'_id': 3})

    # Proof that query works
    for x in testResult:
        print(x)


extract()
