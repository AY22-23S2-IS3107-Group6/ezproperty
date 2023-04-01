#import pymongo
#import pandas as pd
from ..lake import DataLake
from ..warehouse import DataWarehouse
import requests
import json

def extract():

    # Feed data into lake / mongoDB
    print("Test: Feeding data into lake")

    # Test data
    url_property = "https://data.gov.sg/dataset/9dd41b9c-b7d7-405b-88f8-61b9ca9ba224/resource/482bfa14-2977-4035-9c61-c85f871daf4e/data"
    response_property = requests.request("GET", url_property)
    myjson_property = response_property.json()
    data = myjson_property['records']

    db = DataLake()
    db.insert_to_schema("HDB Property Information", data)
    
    transform(data)


def transform(result):

    # Transform data accordingly
    print("Test: Transforming data")

    tempResult = list(result)
    filteredResult = []

    for property in tempResult:
        filteredResult.append(property)

    # need map town to district
    # replacing enum for now

    tag_dict = {"Y": True, "N": False}
    town_dict = {
        "AMK": "ANG MO KIO",
        "BB": "BUKIT BATOK", 
        "BD": "BEDOK",
        "BH": "BISHAN", 
        "BM": "BUKIT MERAH", 
        "BP": "BUKIT PANJANG", 
        "BT": "BUKIT TIMAH", 
        "CCK": "CHOA CHU KANG",
        "CL": "CLEMENTI",
        "CT": "CENTRAL AREA",
        "GL": "GEYLANG", 
        "HG": "HOUGANG",
        "JE": "JURONG EAST", 
        "JW": "JURONG WEST", 
        "KWN": "KALLANG/WHAMPOA",
        "MP": "MARINE PARADE",
        "PG": "PUNGGOL", 
        "PRC": "PASIR RIS", 
        "QT": "QUEENSTOWN", 
        "SB": "SEMBAWANG", 
        "SGN": "SERANGOON",
        "SK": "SENGKANG", 
        "TAP": "TAMPINES", 
        "TG": "TENGAH",
        "TP": "TOA PAYOH", 
        "WL": "WOODLANDS", 
        "YS": "YISHUN"
    }

    for x in filteredResult:

        x["id"] = x["_id"]
        x["block"] = x["blk_no"]
        #x["street"] = x["street"]

        # replacing date with int for now
        x["yearCompleted"] = int(x["year_completed"])

        # integers
        x["totalDwellingUnits"] = int(x["total_dwelling_units"])
        x["maxFloorLevel"] = int(x["max_floor_lvl"])
        x["oneRoomSold"] = int(x["1room_sold"])
        x["twoRoomSold"] = int(x["2room_sold"])
        x["threeRoomSold"] = int(x["3room_sold"])
        x["fourRoomSold"] = int(x["4room_sold"])
        x["fiveRoomSold"] = int(x["5room_sold"])
        x["execSold"] = int(x["exec_sold"])
        x["multigenSold"] = int(x["multigen_sold"])
        x["studioAptSold"] = int(x["studio_apartment_sold"])
        x["oneRoomRental"] = int(x["1room_rental"])
        x["twoRoomRental"] = int(x["2room_rental"])
        x["threeRoomRental"] = int(x["3room_rental"])
        x["otherRoomRental"] = int(x["other_room_rental"])

        # changing tags to booleans
        x["residentialTag"] = tag_dict[x["residential"]]
        x["commercialTag"] = tag_dict[x["commercial"]]
        x["mscpTag"] = tag_dict[x["multistorey_carpark"]]
        x["marketHawkerTag"] = tag_dict[x["market_hawker"]]
        x["precinctPavilionTag"] = tag_dict[x["precinct_pavilion"]]
        x["miscTag"] = tag_dict[x["miscellaneous"]]

        # get town name from acronym
        x["bldgContractTown"] = town_dict[x["bldg_contract_town"]]

        del x['year_completed']
        del x['multigen_sold']
        del x['bldg_contract_town']
        del x['multistorey_carpark']
        del x['total_dwelling_units']
        del x['blk_no']
        del x['exec_sold']
        del x['max_floor_lvl']
        del x['residential']
        del x['1room_sold']
        del x['precinct_pavilion']
        del x['other_room_rental']
        del x['5room_sold']
        del x['3room_sold']
        del x['commercial']
        del x['4room_sold']
        del x['miscellaneous']
        del x['studio_apartment_sold']
        del x['2room_rental']
        del x['2room_sold']
        del x['1room_rental']
        del x['3room_rental']
        del x['market_hawker']
        del x['_id']

    print(result[0])

    load(result)


def load(result):

    # Load data into MySQL accordingly
    print("Test: Loading data")

    result = list(map(lambda x: tuple(x.values()), result))

    print(result[0])

    # Insert data
    db = DataWarehouse(True, False)
    db.insert_to_schema("ref__PropertyInformation", result)

extract()