import pandas as pd
import mysql.connector
import requests
from ..lake import DataLake
from ..warehouse import DataWarehouse


def extract():

    # Fetch data set
    # Seems to be limited by MongoDB's 100 BSON limit
    # resp = requests.get(
    #     'https://data.gov.sg/api/action/datastore_search?resource_id=8f6bba57-19fc-4f36-8dcf-c0bda382364d'
    # )

    resp = requests.get(
        'https://data.gov.sg/api/action/datastore_search?resource_id=8f6bba57-19fc-4f36-8dcf-c0bda382364d&limit=107'
    )

    # print(resp)
    # print(resp.json())
    respHawkerCentre = resp.json()['result']['records']
    # print(respHawkerCentre)

    # Feed data into transformation
    transform(respHawkerCentre)


def transform(respHawkerCentre):

    # need to transform string values of no_of_stalls, no_of_cooked_food_stalls, no_of_mkt_produce_stalls into int
    for record in respHawkerCentre:
        record['no_of_stalls'] = int(record['no_of_stalls'])
        record['no_of_cooked_food_stalls'] = int(
            record['no_of_cooked_food_stalls'])
        record['no_of_mkt_produce_stalls'] = int(
            record['no_of_mkt_produce_stalls'])

    load(respHawkerCentre)


def load(respHawkerCentre):

    # load into mongodb
    db = DataLake()
    db.insert_to_schema("amn__HawkerCentre", respHawkerCentre)

    testResult = db.query_find("amn__HawkerCentre",
                               {"no_of_mkt_produce_stalls": 0})

    # Proof that query works
    for x in testResult:
        print(x)


extract()
