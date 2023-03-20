import pymongo
import pandas as pd
from ..lake import DataLake


def extract():

    # Feed data into lake / mongoDB
    print("Test: Feeding data into lake")

    # Test data
    data = [{ "col1": "row1", "col2": "row2"}]

    db = DataLake()
    db.insert_to_schema("Test collection", data)

    result = db.query("Test collection", [
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



def load(df, table_name):

    print("Bob")

    # Assume we just feed into mongodb first, or do we push into SQL here as well

    # try:
    #     engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
    #         .format(user="",
    #         pw="",
    #         db=""))
        
    #     df.to_sql(table_name, con = engine, if_exists = "append", chunksize = 1000)
    # except Exception as e:
    #     print("Data loading error: " + str(e))


extract()