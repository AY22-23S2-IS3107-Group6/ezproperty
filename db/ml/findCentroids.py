import requests
import pandas as pd
from datetime import date
from ..lake import DataLake
from ..warehouse import DataWarehouse
import json


# Define the JSON object
# Private Residential Properties Rental Contract
def findCentroids():

    # Feed data into lake / mongoDB
    print("Test: Feeding data into lake")

    # Test data
    data = [{"_id": 0, "col1": 2, "col2": 3}]
    # data = [{"_id": "1", "col1": "row1", "col2": "row2"}]

    db = DataLake()
    db.insert_to_schema("Test collection", data)

    result = db.query("Test collection", [{
        "$match": {
            "col1": 2
        }
    }, {
        "$project": {
            "_id": 0,
            "col2": 1
        }
    }])

    # Proof that query works
    for x in result:
        print(x)

    print("Test: Loading data")

    result = list(map(lambda x: tuple(x.values()), data))

    print(result)

    # Test data
    print("Test: Feeding data into lake")

    insert_data = [{'district': 1, 'x': 12345, 'y': 67899}]

    db = DataLake()
    db.insert_to_schema("Test collection", insert_data)

    result = db.query("Test collection", [{
        "$match": {
            "district": 1
        }
    }, {
        "$project": {
            "x": 12345,
            "y": 67899
        }
    }])

    db = DataWarehouse()
    print("Test: sql data")
    db.insert_to_schema("test__Test2", result)

    insert_data = [{'district': 2, 'x': 11111, 'y': 22222}]
    result = list(map(lambda x: tuple(x.values()), insert_data))
    db.insert_to_schema("test__Test2", result)

    data = db.query('''
      SELECT district, x, y FROM main__PropertyTransaction
    ''')

    # Create a dictionary to store the total x and y values and number of properties for each district
    district_data = {}

    # Iterate through the properties and calculate the total x and y values for each district
    for row in data:
        # need to accomodate to rental or transaction or rentalMedian
        #  also cases when district is separate
        district = row["district"]
        x = row["x"]
        y = row["y"]

        if district not in district_data:
            district_data[district] = {"x_total": x, "y_total": y, "count": 1}
        else:
            district_data[district]["x_total"] += x
            district_data[district]["y_total"] += y
            district_data[district]["count"] += 1

    # Iterate through the districts and calculate the average x and y values

    district_centroid = {}

    for district, data in district_data.items():
        # data is the array within each dictionary
        x_avg = data["x_total"] / data["count"]
        y_avg = data["y_total"] / data["count"]
        district_centroid[district] = {"x_avg": x_avg, "y_avg": y_avg}

        print("District:", district)
        print("Average x value and y value", district_centroid[district])
        # print("Average y value:", y_avg)
    return district_centroid


findCentroids()
