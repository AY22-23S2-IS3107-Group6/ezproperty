import requests
from sqlalchemy import create_engine
import json
import pandas as pd
from ..lake import DataLake
from ..warehouse import DataWarehouse
import math
import findCentroids


def assignDistricts(district_centroid):

    # df represents dataframe queried from sql
    db = DataWarehouse()
    data = db.query('''
      SELECT district, x, y FROM main__PropertyTransaction OFFSET 3
    ''')

    # iterating through df
    for row in data:
        shortest_dist = -1
        closest_district = -1
        x = row['x']
        y = row['y']

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

        row_id = row['id']
        db.update('''
            UPDATE main__PropertyTransaction SET district = closest_district WHERE id = row_id
        ''')

    # use Sean's update function to update sql district?


assignDistricts(findCentroids.findCentroids())
