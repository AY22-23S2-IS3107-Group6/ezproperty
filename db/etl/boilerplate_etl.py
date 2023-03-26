import pymongo
import pandas as pd
from ..lake import DataLake
from ..warehouse import DataWarehouse

def extract():

    # Feed data into lake / mongoDB
    print("Test: Feeding data into lake")

    # Test data
    data = [{ "_id": "1", "col1": "row1", "col2": "row2"}]

    db = DataLake()
    db.insert_to_schema("Test collection", data)

    result = db.query("amn__Carpark", [
        {"$match": {"col1": "row1"}},
        {"$project": {"_id": 0, "col2": 1}}
    ])

    # Proof that query works
    for x in result:
        print(x)
    
    transform(result)


def transform(result):

    # Transform data accordingly
    print("Test: Transforming data")

    load(result)


def load(result):

    # Load data into MySQL accordingly
    print("Test: Loading data")
    print(result)

    # result = list(map(lambda x: tuple(x.values()), result))
    result = result.map(lambda x: tuple(x.values()))
    

    print(result)

    # Insert data
    db = DataWarehouse()
    db.insert_to_schema("test__Test", result)

    # Query data using SQL
    result = db.query('''
        SELECT * FROM test__Test
    ''')

    for x in result:
        print(x)


extract()