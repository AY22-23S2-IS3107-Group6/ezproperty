import pymongo
import pandas as pd
from ..lake import DataLake
from ..warehouse import DataWarehouse

# Other thoughts
# Where does the data init into mongodb happen? Assuming it's from data_loader or is it airflow? But I'll need to look more into airflow functionality first. Need to prevent duplicate inputs in. Then extract will just fetch from mongodb.
# Added a find query along with aggregate into DataLake
# Installations - need to make sure have correct ones
# Updated readme - there was missing argument for collection name for db.query
# Calling the file - python3 -m db.etl.boilerplate_etl
# __init__.py for warehouse - updated create_table function call to create_schema
# schemas - ive commented out your schemas, but just need to make sure they can run properly

def extract():

    # Feed data into lake / mongoDB
    print("Test: Feeding data into lake")

    # Test data
    data = [{ "_id": "1", "col1": "row1", "col2": "row2"}]

    db = DataLake()
    db.insert_to_schema("Test collection", data)

    result = db.query("Test collection", [
        {"$match": {"col1": "row1"}},
        {"$project": {"_id": 0, "col2": 1}}
    ])

    # Proof that query works
    for x in result:
        print(x)
    
    transform(data)


def transform(result):

    # Transform data accordingly
    print("Test: Transforming data")

    load(result)


def load(result):

    # Load data into MySQL accordingly
    print("Test: Loading data")

    result = list(map(lambda x: tuple(x.values()), result))

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