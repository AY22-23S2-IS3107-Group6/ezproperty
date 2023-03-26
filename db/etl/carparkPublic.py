import pymongo
import pandas as pd
import requests
import json
from ..lake import DataLake
from ..warehouse import DataWarehouse


def extract():

    # Feed data into lake / mongoDB
    print("Carpark Public: Feeding data into lake")

    URA_API_ACCESSKEY = '84d7c27b-8dc6-4a34-9ea3-7769c174007c'

    # Fetches daily token which is needed along with access key for API calls
    fetchTokenHeader = {'Content-Type': 'application/json', 'AccessKey': URA_API_ACCESSKEY, 'Accept': 'application/json', 'User-Agent': 'PostmanRuntime/7.28.4'} # returns html without user agent postman
    resp = requests.get('https://www.ura.gov.sg/uraDataService/insertNewToken.action', headers = fetchTokenHeader) 

    print(resp)
    print(resp.json())

    URA_API_TOKEN = resp.json()['Result']

    # Setting up default header for API calls
    apiHeader = {'Content-Type': 'application/json', 'AccessKey': URA_API_ACCESSKEY, 'Token': URA_API_TOKEN, 'User-Agent': 'PostmanRuntime/7.30.1'}

    # Fetch both data sets
    respPublic = requests.get('https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details', headers = apiHeader)
    # respSeason = requests.get('https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Season_Car_Park_Details', headers = apiHeader) 

    carparkPublic = respPublic.json()['Result']
    # carparkSeason = respSeason.json()['Result']

    # Insert data
    db = DataLake()
    # db.insert_to_schema("amn__CarparkPublic", carparkPublic) UNCOMMENT LATER
    # db.insert_to_schema("amn__CarparkSeason", carparkSeason)

    # Test query
    testResult = db.query_find("amn__CarparkPublic", 
        { "ppCode": "A0004" }
    )

    # Proof that query works
    for x in testResult:
        print(x)

    # Query to get data - not super needed since currently fetching all, but just in case want to modify query
    result = db.query_find("amn__CarparkPublic", 
        {}
    )
    
    transform(result)


def transform(result):
   
    # Transform data accordingly
    print("Carpark Public: Transforming data")

    temp = list(result)
    filteredCarparks = []

    # Remove carparks with missing geometry or coordinates
    for carpark in temp:
        if 'geometries' in carpark:
            if carpark['geometries'] != []:
                filteredCarparks.append(carpark)

    # Flatten coordinates
    # Bring out into x and y key
    for carpark in filteredCarparks:
        carpark['x'] = float(carpark['geometries'][0]['coordinates'].split(",")[0])
        carpark['y'] = float(carpark['geometries'][0]['coordinates'].split(",")[1])
        del carpark['geometries']

    # Typecast appropriately to feed into sql
    for carpark in filteredCarparks:
        carpark['weekdayRate'] = float(carpark['weekdayRate'][1:]) # removing $ sign
        carpark['weekdayMin'] = int(carpark['weekdayMin'][:-5]) # removing mins from back
        carpark['satdayRate'] = float(carpark['satdayRate'][1:])
        carpark['satdayMin'] = int(carpark['satdayMin'][:-5])
        carpark['sunPHRate'] = float(carpark['sunPHRate'][1:])
        carpark['sunPHMin'] = int(carpark['sunPHMin'][:-5])

    print(filteredCarparks[0])

    # Merge objects with ppCode - hold off for now; prob better to minimise transformation and see what's needed during analyiss maybe
    # prob use double for loop and update function to merge

    load(filteredCarparks)


def load(result):

    # Load data into MySQL accordingly
    print("Carpark Public: Loading data")

    # result = result.map(lambda x: tuple(x.values()))

    # print(result)

    # Insert data
    db = DataWarehouse()
    # db.insert_to_schema("amn__CarparkPublic", result)

    # # Query data using SQL
    # result = db.query('''
    #     SELECT * FROM test__Test
    # ''')

    # for x in result:
    #     print(x)




extract()


