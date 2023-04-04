import pandas as pd
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

    result = resp.json()['result']['records']

    db = DataLake()
    db.insert_to_schema("amn__HawkerCentre", result)
    result = db.query_find("amn__HawkerCentre", {})

    # Feed data into transformation
    transform(result)


def transform(result):

    result = list(result)

    # need to transform string values of noOfStalls, noOfCookedFoodStalls, noOfMktProduceStalls into int
    for record in result:
        del record['_id']
        record['name'] = record['name_of_centre']
        del record['name_of_centre']
        record['location'] = record['location_of_centre']
        del record['location_of_centre']
        record['type'] = record['type_of_centre']
        del record['type_of_centre']
        owner = record['owner']
        del record['owner']
        record['owner'] = owner
        record['noOfStalls'] = int(record['no_of_stalls'])
        del record['no_of_stalls']
        record['noOfCookedFoodStalls'] = int(record['no_of_cooked_food_stalls'])
        del record['no_of_cooked_food_stalls']
        record['noOfMktProduceStalls'] = int(record['no_of_mkt_produce_stalls'])
        del record['no_of_mkt_produce_stalls']
        record['district'] = None

    load(result)


def load(result):

    print("Hawker Centre: Loading data")
    
    result = list(map(lambda x: tuple(x.values()), result))

    # Insert data
    db = DataWarehouse()
    db.insert_to_schema("amn__HawkerCentre", result)

    # Query data using SQL
    result = db.query('''
        SELECT * FROM amn__HawkerCentre
    ''')
    print(result[0])


extract()
