import requests
from sqlalchemy import create_engine
import json
import pandas as pd
from ..lake import DataLake
from ..warehouse import DataWarehouse
import math


def assignDistricts():

    district_centroid = {}

    # df represents dataframe queried from sql
    # iterating through df
    for row in df.itertuples():
        shortest_dist = -1
        closest_district = -1
        x = row['x']
        y = row['y']

        for district in district_centroid.items():

            x_dist = math.sqrt(abs(x**2 - district["x_avg"]**2))
            y_dist = math.sqrt(abs(y**2 - district["y_avg"]**2))
            dist = x_dist + y_dist
            if shortest_dist == -1:
                shortest_dist = dist
                closest_district = district  # this is returning tuple, not the value of district
            elif dist < shortest_dist:
                shortest_dist = dist
                closest_district = district  # this is returning tuple, not the value of district

    # use Sean's update function to update sql district?

    # JSON implementation
    # Parse the JSON object into a Python dictionary
    data = json.loads(private_properties_rental_contract_json_str)

    # Create a dictionary to store the total x and y values and number of properties for each district
    district_data = {}

    # Iterate through the properties and calculate the total x and y values for each district
    for property in data["Result"]:
        # need to accomodate to rental or transaction or rentalMedian
        #  also cases when district is separate
        district = property["rental"][0]["district"]
        x = float(property["x"])
        y = float(property["y"])

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


findCentroids()
