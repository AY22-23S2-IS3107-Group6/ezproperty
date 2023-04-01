#import pymongo
#import pandas as pd
from ..lake import DataLake
from ..warehouse import DataWarehouse
import requests
import json

def extract():

    # Feed data into lake / mongoDB
    print("Test: Feeding data into lake")

    # Data
    data = [
        {"district": 1, "towns": "Raffles Place, Cecil, Marina, People's Park", "postalCodeStart": 1, "postalCodeEnd": 6},
        {"district": 2, "towns": "Anson, Tanjong Pagar", "postalCodeStart": 7, "postalCodeEnd": 8},
        {"district": 3, "towns": "Queenstown, Tiong Bahru", "postalCodeStart": 14, "postalCodeEnd": 16},
        {"district": 4, "towns": "Telok Blangah, Harbourfront", "postalCodeStart": 9, "postalCodeEnd": 10},
        {"district": 5, "towns": "Pasir Panjang, Hong Leong Garden, Clementi New Town", "postalCodeStart": 11, "postalCodeEnd": 13},
        {"district": 6, "towns": "High Street, Beach Road (part)", "postalCodeStart": 17, "postalCodeEnd": 17},
        {"district": 7, "towns": "Middle Road, Golden Mile", "postalCodeStart": 18, "postalCodeEnd": 19},
        {"district": 8, "towns": "Little India", "postalCodeStart": 20, "postalCodeEnd": 21},
        {"district": 9, "towns": "Orchard, Cairnhill, River Valley", "postalCodeStart": 22, "postalCodeEnd": 23},
        {"district": 10, "towns": "Ardmore, Bukit Timah, Holland Road, Tanglin", "postalCodeStart": 24, "postalCodeEnd": 27},
        {"district": 11, "towns": "Watten Estate, Novena, Thomson", "postalCodeStart": 28, "postalCodeEnd": 30},
        {"district": 12, "towns": "Balestier, Toa Payoh, Serangoon", "postalCodeStart": 31, "postalCodeEnd": 33},
        {"district": 13, "towns": "Macpherson, Braddell", "postalCodeStart": 34, "postalCodeEnd": 37},
        {"district": 14, "towns": "Geylang, Eunos", "postalCodeStart": 38, "postalCodeEnd": 41},
        {"district": 15, "towns": "Katong, Joo Chiat, Amber Road", "postalCodeStart": 42, "postalCodeEnd": 45},
        {"district": 16, "towns": "Bedok, Upper East Coast, Eastwood, Kew Drive", "postalCodeStart": 46, "postalCodeEnd": 48},
        {"district": 17, "towns": "Loyang, Changi", "postalCodeStart": 49, "postalCodeEnd": 50},
        {"district": 17, "towns": "Loyang, Changi", "postalCodeStart": 81, "postalCodeEnd": 81},
        {"district": 18, "towns": "Tampines, Pasir Ris", "postalCodeStart": 51, "postalCodeEnd": 52},
        {"district": 19, "towns": "Serangoon Garden, Hougang, Punggol", "postalCodeStart": 53, "postalCodeEnd": 55},
        {"district": 19, "towns": "Serangoon Garden, Hougang, Punggol", "postalCodeStart": 82, "postalCodeEnd": 82},
        {"district": 20, "towns": "Bishan, Ang Mo Kio", "postalCodeStart": 56, "postalCodeEnd": 57},
        {"district": 21, "towns": "Upper Bukit Timah, Clementi Park, Ulu Pandan", "postalCodeStart": 58, "postalCodeEnd": 59},
        {"district": 22, "towns": "Jurong", "postalCodeStart": 60, "postalCodeEnd": 64},
        {"district": 23, "towns": "Hillview, Dairy Farm, Bukit Panjang, Choa Chu Kang", "postalCodeStart": 65, "postalCodeEnd": 68},
        {"district": 24, "towns": "Lim Chu Kang, Tengah", "postalCodeStart": 69, "postalCodeEnd": 71},
        {"district": 25, "towns": "Kranji, Woodgrove", "postalCodeStart": 72, "postalCodeEnd": 73},
        {"district": 26, "towns": "Upper Thomson, Springleaf", "postalCodeStart": 77, "postalCodeEnd": 78},
        {"district": 27, "towns": "Yishun, Sembawang", "postalCodeStart": 75, "postalCodeEnd": 76},
        {"district": 28, "towns": "Seletar", "postalCodeStart": 79, "postalCodeEnd": 80}
    ]

    db = DataLake()
    db.insert_to_schema("ref__District", data)
    
    transform(data)


def transform(result):

    # Transform data accordingly
    print("Test: Transforming data")

    # no x and y values yet

    for x in result:
        del x['_id']

    load(result)


def load(result):

    # Load data into MySQL accordingly
    print("Test: Loading data")

    print(result)

    result = list(map(lambda x: tuple(x.values()), result))

    print(result[0])

    # Insert data
    db = DataWarehouse(True, False)
    db.insert_to_schema("ref__District", result)

extract()