import pandas as pd
import requests
from ..lake import DataLake
from ..warehouse import DataWarehouse


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

    result = resp.json()['result']['records']

    db = DataLake()
    db.insert_to_schema("amn__Supermarket", result)
    result = db.query_find("amn__Supermarket", {})

    # Feed data into transformation
    transform(result)


def transform(result):
    result = list(result)

    # need to transform string values of noOfStalls, noOfCookedFoodStalls, noOfMktProduceStalls into int
    for record in result:
        del record['_id']
        record['licenceNo'] = record['licence_num']
        del record['licence_num']
        record['licenseeName'] = record['licensee_name']
        del record['licensee_name']
        record['buildingName'] = record['building_name']
        del record['building_name']
        record['blockHouseNo'] = record['block_house_num']
        del record['block_house_num']
        record['level'] = record['level_num']
        del record['level_num']
        record['unitNo'] = record['unit_num']
        del record['unit_num']
        record['streetName'] = record['street_name']
        del record['street_name']
        record['postalCode'] = int(record['postal_code'])
        del record['postal_code']
        record['district'] = None

    load(result)


def load(result):

    print("Hawker Centre: Loading data")
    
    result = list(map(lambda x: tuple(x.values()), result))

    # Insert data
    db = DataWarehouse()
    db.insert_to_schema("amn__Supermarket", result)

    # Query data using SQL
    result = db.query('''
        SELECT * FROM amn__Supermarket
    ''')
    print(result[0])


extract()
