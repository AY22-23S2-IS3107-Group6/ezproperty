import requests
import pandas as pd
from datetime import date
from ..lake import DataLake
from ..warehouse import DataWarehouse
import json
import math


# Define the JSON object
# Private Residential Properties Rental Contract
def findCentroids():

    db = DataWarehouse()

    data = db.query('''
      SELECT district, x, y FROM main__PropertyTransaction WHERE _id > 3
    ''')

    # Create a dictionary to store the total x and y values and number of properties for each district
    district_data = {}

    # Iterate through the properties and calculate the total x and y values for each district
    for row in data:
        # need to accomodate to rental or transaction or rentalMedian
        #  also cases when district is separate
        district = row[0]
        x = row[1]
        y = row[2]

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

    assignDistricts(district_centroid)


def assignDistricts(district_centroid):

    # df represents dataframe queried from sql
    db = DataWarehouse()
    data = db.query('''
      SELECT _id, district, x, y FROM main__PropertyTransaction WHERE _id  <= 3
    ''')

    # iterating through df
    for row in data:
        shortest_dist = -1
        closest_district = -1
        x = row[2]
        y = row[3]

        for district, data in district_centroid.items():

            x_dist = ((x - data["x_avg"])**2)
            y_dist = ((y - data["y_avg"])**2)
            dist = math.sqrt(x_dist + y_dist)
            if shortest_dist == -1:
                shortest_dist = dist
                closest_district = district
            elif dist < shortest_dist:
                shortest_dist = dist
                closest_district = district

        row_id = row[0]
        print("new district for row " + str(row_id) + " is " +
              str(closest_district))
        db.update(
            '''
            UPDATE main__PropertyTransaction SET district = %s WHERE _id = %s
        ''', (closest_district, row_id))


findCentroids()